/* Orçamento em 2 etapas → resumo vivo → WhatsApp ou e-mail. Validação inline, rascunho guardado na sessão. */
(function () {
  'use strict';
  var D = document, SP = window.SP, form = D.getElementById('qform');
  if (!form || !SP) return;
  var $ = function (s) { return form.querySelector(s); }, $$ = function (s) { return [].slice.call(form.querySelectorAll(s)); };
  var step2 = D.getElementById('step2'), err1 = D.getElementById('err1'), errS = D.getElementById('errS');
  var waBtn = D.getElementById('sendWa'), mailBtn = D.getElementById('sendMail'), list = D.getElementById('sumList');
  var stBox = D.getElementById('qSticky'), stBtn = D.getElementById('qStickyBtn'), stTxt = D.getElementById('qStickyTxt');
  if (stBtn) { stBtn.target = '_blank'; stBtn.rel = 'noopener'; }
  var started = false, KEY = 'sp_quote', sumLive = D.getElementById('sumLive'), liveT = 0;

  function one(n) { var r = form.querySelector('input[name="' + n + '"]:checked'); return r ? r.value : ''; }
  function many(n) { return $$('input[name="' + n + '"]:checked').map(function (i) { return i.value; }); }
  function val(n) { var el = form.elements[n]; return el ? String(el.value || '').trim() : ''; }
  function num(n, d) { var v = parseFloat(String(val(n)).replace(',', '.')); return isNaN(v) ? d : v; }
  function fmt(n, d) { return n.toLocaleString('pt-BR', { minimumFractionDigits: d == null ? 1 : d, maximumFractionDigits: d == null ? 2 : d }); }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function data() {
    var w = num('w', 0), h = num('h', 0), q = Math.max(1, Math.round(num('q', 1))), date = val('data'), days = null;
    if (date) { var d = new Date(date + 'T12:00:00'), now = new Date(); now.setHours(12, 0, 0, 0); days = Math.round((d - now) / 86400000); }
    return { perfil: one('perfil'), produtos: many('produto'), nome: val('nome'), empresa: val('empresa'), w: w, h: h, q: q, sized: w > 0 && h > 0, date: date, days: days,
      local: val('local'), inst: one('inst'), arte: one('arte'), detalhe: val('detalhe'), origem: one('origem') || SP.attr.utm_source || '' };
  }
  function left(n) { return n === 0 ? 'é hoje' : n === 1 ? 'falta 1 dia' : 'faltam ' + n + ' dias'; }
  function dateBR(s) { var p = s.split('-'); return p.length === 3 ? p[2] + '/' + p[1] + '/' + p[0] : s; }
  function rows(d) {
    var r = [['Perfil', d.perfil || 'A escolher'], ['Produtos', d.produtos.join(', ') || 'A escolher']];
    if (d.sized) r.push(['Medida', fmt(d.w) + ' × ' + fmt(d.h) + ' m · ' + d.q + ' un.']);
    if (d.date) r.push(['Evento', dateBR(d.date) + (d.days != null && d.days >= 0 ? ' · ' + left(d.days) : '')]);
    if (d.local) r.push(['Local', d.local]);
    if (d.inst) r.push(['Instalação', d.inst]);
    if (d.arte) r.push(['Arte', d.arte]);
    return r;
  }
  function message(d) {
    var l = ['Olá, Smart Pix! Quero um orçamento.'];
    if (d.perfil) l.push('• Perfil: ' + d.perfil);
    if (d.produtos.length) l.push('• Produtos: ' + d.produtos.join(', '));
    if (d.sized) l.push('• Medida: ' + fmt(d.w) + ' × ' + fmt(d.h) + ' m · ' + d.q + ' un. · ' + fmt(d.w * d.h * d.q) + ' m²');
    if (d.date) l.push('• Data do evento: ' + dateBR(d.date) + (d.days != null && d.days >= 0 ? ' (' + left(d.days) + ')' : ''));
    if (d.local) l.push('• Local: ' + d.local);
    if (d.inst) l.push('• Instalação: ' + d.inst);
    if (d.arte) l.push('• Arte: ' + d.arte);
    if (d.detalhe) l.push('• Detalhes: ' + d.detalhe);
    if (d.nome) l.push('• Nome: ' + d.nome + (d.empresa ? ' (' + d.empresa + ')' : ''));
    if (d.origem) l.push('• Origem: ' + d.origem);
    l.push('(enviado pelo site)');
    return l.join('\n');
  }
  function missing(d) { var m = []; if (!d.perfil) m.push('o seu perfil'); if (!d.produtos.length) m.push('o produto'); if (!d.nome) m.push('o seu nome'); return m; }

  function update() {
    var d = data();
    list.innerHTML = rows(d).map(function (r) { return '<dt>' + esc(r[0]) + '</dt><dd>' + esc(r[1]) + '</dd>'; }).join('');
    var area = D.getElementById('sumArea'); area.textContent = d.sized ? fmt(d.w * d.h * d.q) + ' m²' : 'a definir'; area.classList.toggle('empty', !d.sized);
    clearTimeout(liveT); liveT = setTimeout(function () { var t = 'Resumo: ' + (d.produtos.length ? d.produtos.length + (d.produtos.length === 1 ? ' produto' : ' produtos') : 'nenhum produto') + (d.sized ? ', ' + fmt(d.w * d.h * d.q) + ' m²' : '') + '.'; if (sumLive.textContent !== t) sumLive.textContent = t; }, 900);
    if (stBtn) { stBtn.href = SP.waLink(message(d)); stTxt.textContent = (d.produtos.length ? d.produtos.join(', ') : 'Resumo do pedido') + (d.sized ? ' · ' + fmt(d.w * d.h * d.q) + ' m²' : ''); }
    var seam = D.getElementById('seam'), lona = d.produtos.some(function (p) { return /Lona|Estande/.test(p); });
    seam.hidden = !(lona && d.sized); if (!seam.hidden) { var ok = Math.min(d.w, d.h) <= 5; seam.className = 'badge' + (ok ? '' : ' warn'); seam.textContent = ok ? 'Cabe numa peça só: até 5 m de largura sem emenda.' : 'Acima de 5 m nos dois lados, a lona é feita em partes.'; }
    var urg = D.getElementById('urgent'); urg.hidden = !(d.days != null && d.days >= 0 && d.days <= 7);
    var past = D.getElementById('past'); past.hidden = !(d.days != null && d.days < 0);
    var msg = message(d);
    waBtn.href = SP.waLink(msg);
    mailBtn.href = 'mailto:atendimento@smartpix.com.br?subject=' + encodeURIComponent('Orçamento pelo site' + (d.empresa ? ' · ' + d.empresa : '')) + '&body=' + encodeURIComponent(msg);
    if (errS.textContent && !missing(d).length) errS.textContent = '';
    if (err1.textContent && !missing(d).length) err1.textContent = '';
    if (d.nome) form.elements.nome.removeAttribute('aria-invalid'); if (d.perfil) $$('input[name=perfil]').forEach(function (i) { i.removeAttribute('aria-invalid'); }); if (d.produtos.length) $$('input[name=produto]').forEach(function (i) { i.removeAttribute('aria-invalid'); });
    save();
  }
  function save() { try { var o = {}; $$('input,textarea,select').forEach(function (i) { if (!i.name) return; if (i.type === 'radio') { if (i.checked) o[i.name] = i.value; } else if (i.type === 'checkbox') { if (i.checked) (o[i.name] = o[i.name] || []).push(i.value); } else o[i.name] = i.value; }); o._s2 = !step2.hidden; sessionStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {} }
  function restore() { try { var o = JSON.parse(sessionStorage.getItem(KEY) || 'null'); if (!o) return; $$('input,textarea,select').forEach(function (i) { if (!(i.name in o)) return; if (i.type === 'radio') i.checked = o[i.name] === i.value; else if (i.type === 'checkbox') i.checked = [].concat(o[i.name]).indexOf(i.value) > -1; else i.value = o[i.name]; }); if (o._s2) show2(false); } catch (e) {} }

  function show2(focus) {
    step2.hidden = false; D.getElementById('st2').classList.add('on'); D.getElementById('stTxt').textContent = 'Etapa 2 de 2 · Detalhes'; D.getElementById('goStep2').hidden = true;
    if (focus) { setTimeout(function () { step2.scrollIntoView({ behavior: SP.reduce ? 'auto' : 'smooth', block: 'start' }); step2.focus({ preventScroll: true }); }, 30); }
    SP.track('quote_step', { step: 2 });
  }
  function check(where) {
    var d = data(), m = missing(d); if (!m.length) return true;
    var msg = 'Falta ' + m.join(', ').replace(/, ([^,]*)$/, ' e $1') + ' para montar o pedido.';
    var box = where === 1 ? err1 : errS; box.textContent = ''; setTimeout(function () { box.textContent = msg; }, 30);
    if (!d.nome) form.elements.nome.setAttribute('aria-invalid', 'true'); if (!d.perfil) $('input[name=perfil]').setAttribute('aria-invalid', 'true'); if (!d.produtos.length) $('input[name=produto]').setAttribute('aria-invalid', 'true');
    var first = !d.perfil ? $('input[name=perfil]') : !d.produtos.length ? $('input[name=produto]') : form.elements.nome; first.focus();
    SP.track('quote_error', { missing: m.join(',') });
    return false;
  }

  /* prefill from links (Estúdio 3D, problems, product pages) */
  try {
    var q = new URLSearchParams(location.search), extra = [];
    if (q.get('produto')) q.get('produto').split('|').forEach(function (p) { var i = $$('input[name=produto]').filter(function (x) { return x.value === p; })[0]; if (i) i.checked = true; });
    if (q.get('perfil')) { var pi = $$('input[name=perfil]').filter(function (x) { return x.value === q.get('perfil'); })[0]; if (pi) pi.checked = true; }
    if (q.get('marca')) extra.push('Marca: ' + q.get('marca') + (q.get('cor') ? ', cor ' + q.get('cor').toLowerCase() : '') + ' (montei no Estúdio 3D do site)');
    if (q.get('problema')) extra.push('Quero resolver: ' + q.get('problema'));
    if (extra.length && !val('detalhe')) form.elements.detalhe.value = extra.join('. ') + '.';
    if (q.get('origem')) SP.track('quote_prefill', { from: q.get('origem') });
  } catch (e) {}
  if (!location.search) restore();

  form.addEventListener('input', function () { if (!started) { started = true; SP.track('quote_start'); } update(); });
  form.addEventListener('change', update);
  form.addEventListener('submit', function (e) { e.preventDefault(); });
  form.addEventListener('click', function (e) {
    var b = e.target.closest('[data-step]'); if (!b) return;
    var el = form.elements[b.getAttribute('data-step')], d = parseFloat(b.getAttribute('data-d')), cur = parseFloat(String(el.value).replace(',', '.')) || 0;
    var k = b.getAttribute('data-step'); el.value = k === 'q' ? Math.max(1, Math.round(cur + d)) : Math.max(0, Math.round((cur + d) * 10) / 10); update();
    SP.say && SP.say((k === 'w' ? 'Largura: ' : k === 'h' ? 'Altura: ' : 'Quantidade: ') + (k === 'q' ? el.value + ' unidades' : fmt(+el.value) + ' m'));
  });
  D.getElementById('goStep2').addEventListener('click', function () { if (check(1)) show2(true); });
  function send(method) { return function (e) { if (!check('s')) { e.preventDefault(); return; } update(); var d = data(); if (method === 'whatsapp') { var st = D.getElementById('sent'); st.hidden = false; } SP.track('generate_lead', { method: method, perfil: d.perfil, produtos: d.produtos.join('|'), area_m2: d.sized ? +(d.w * d.h * d.q).toFixed(2) : 0, days_to_event: d.days, installation: d.inst || 'n/a', lead_source: d.origem || 'n/a' }); }; }
  waBtn.addEventListener('click', send('whatsapp'));
  mailBtn.addEventListener('click', send('email'));
  if (stBtn) stBtn.addEventListener('click', send('whatsapp'));
  /* the phone send bar shows once the visitor starts and hides while the summary itself is on screen */
  if (stBox && 'IntersectionObserver' in window) {
    var sumVis = false, sumEl = D.getElementById('resumo');
    function stUpdate() { var on = started && !sumVis; stBox.classList.toggle('on', on); stBox.setAttribute('aria-hidden', !on); stBtn.tabIndex = on ? 0 : -1; }
    new IntersectionObserver(function (es) { sumVis = es[0].isIntersecting; stUpdate(); }, { threshold: 0.15 }).observe(sumEl);
    form.addEventListener('input', stUpdate); form.addEventListener('change', stUpdate);
  }
  var cm = D.getElementById('copyMsg');
  if (cm) cm.addEventListener('click', function () { var t = message(data()); try { navigator.clipboard.writeText(t).then(function () { cm.textContent = 'Mensagem copiada'; SP.say('Mensagem copiada'); setTimeout(function () { cm.textContent = 'Copiar mensagem'; }, 1800); }, function () {}); } catch (e) {} SP.track('copy', { what: 'quote_message' }); });
  /* earliest date is today in the visitor's time zone (toISOString is UTC: after 21h in Brazil it would already be tomorrow) */
  var dateEl = form.elements.data; if (dateEl) { var t = new Date(), two = function (n) { return (n < 10 ? '0' : '') + n; }; dateEl.min = t.getFullYear() + '-' + two(t.getMonth() + 1) + '-' + two(t.getDate()); }
  update();
})();

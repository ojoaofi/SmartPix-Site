/* Problemas que resolvemos: card gallery. The + turns a card from the problem to the solution and back.
   Both faces stay in the DOM; only the visible one is exposed to assistive tech and the tab order. */
(function () {
  'use strict';
  var D = document, SP = window.SP;
  D.querySelectorAll('.pc').forEach(function (card) {
    var btn = card.querySelector('.pc-toggle'), back = card.querySelector('.pc-back'), label = btn.querySelector('.sr'), title = card.querySelector('.pc-title').textContent.replace(/\.$/, '').toLowerCase();
    function set(open) {
      card.classList.toggle('open', open);
      btn.setAttribute('aria-expanded', open);
      back.setAttribute('aria-hidden', !open); back.inert = !open;
      label.textContent = open ? 'Voltar ao problema: ' + title : 'Ver como resolvemos: ' + title;
      if (open && SP) SP.track('problem_view', { problem: card.id.replace('pc-', '') });
    }
    btn.addEventListener('click', function () { set(!card.classList.contains('open')); });
    card.addEventListener('keydown', function (e) { if (e.key === 'Escape' && card.classList.contains('open')) { set(false); btn.focus(); } });
  });
})();

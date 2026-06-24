/* ============================================================
   KIZZ HAIR — main.js
   ローディング / ハンバーガーメニュー / FAQアコーディオン / スクロール表示
   ============================================================ */
(function () {
  'use strict';

  document.documentElement.lang = 'ja';

  /* ---- Loading overlay (初回のみ) ---- */
  var loader = document.getElementById('loader');
  if (loader) {
    var seen = false;
    try { seen = sessionStorage.getItem('kizz_seen') === '1'; } catch (e) {}
    if (seen) {
      loader.parentNode && loader.parentNode.removeChild(loader);
    } else {
      try { sessionStorage.setItem('kizz_seen', '1'); } catch (e) {}
      window.setTimeout(function () { loader.classList.add('is-hidden'); }, 1700);
      loader.addEventListener('transitionend', function () {
        if (loader.parentNode) loader.parentNode.removeChild(loader);
      });
    }
  }

  /* ---- Mobile fullscreen menu ---- */
  var menu = document.getElementById('menu');
  var openBtn = document.getElementById('menuOpen');
  var closeBtn = document.getElementById('menuClose');
  function openMenu()  { if (menu) menu.hidden = false; }
  function closeMenu() { if (menu) menu.hidden = true; }
  if (openBtn) openBtn.addEventListener('click', openMenu);
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (menu) {
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeMenu);
    });
  }

  /* ---- FAQ accordion ---- */
  document.querySelectorAll('.faq__q').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq');
      if (!item) return;
      var isOpen = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  });

  /* ---- Scroll reveal ---- */
  var reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && reveals.length) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('is-in');
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.12 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add('is-in'); });
  }
})();

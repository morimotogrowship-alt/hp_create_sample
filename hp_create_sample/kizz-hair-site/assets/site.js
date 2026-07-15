const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];

window.addEventListener('DOMContentLoaded', () => {
  /* ---- Loading ---- */
  const loader = $('.loader');
  if (loader) {
    if (sessionStorage.getItem('kizzSeen')) {
      loader.classList.add('hide');
    } else {
      sessionStorage.setItem('kizzSeen', '1');
      setTimeout(() => loader.classList.add('hide'), 1750);
    }
  }

  /* ---- Mobile menu ---- */
  const hamburger = $('.hamburger');
  const mobileMenu = $('.mobile-menu');
  const mobileClose = $('.mobile-close');

  const openMenu = () => {
    mobileMenu.classList.add('open');
    hamburger.setAttribute('aria-expanded', 'true');
  };
  const closeMenu = () => {
    mobileMenu.classList.remove('open');
    hamburger.setAttribute('aria-expanded', 'false');
  };

  hamburger?.addEventListener('click', () =>
    mobileMenu.classList.contains('open') ? closeMenu() : openMenu()
  );
  mobileClose?.addEventListener('click', closeMenu);
  $$('.mobile-menu a').forEach(a => a.addEventListener('click', closeMenu));

  /* ---- FAQ accordion ---- */
  $$('.faq-q').forEach(btn => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      $$('.faq-item').forEach(i => i.classList.remove('open'));
      if (!isOpen) item.classList.add('open');
    });
  });

  /* ---- Snap scroll for full-screen sections ---- */
  initSnap();
});

function initSnap() {
  const snapPage = $('.page.snap');
  if (!snapPage) return;
  const sections = $$('.fs', snapPage).slice(0, 3);
  if (sections.length < 3) return;

  let busy = false;
  let touchY = 0;
  const WHEEL_MIN = 30;
  const TOUCH_MIN = 48;

  const clamp = i => Math.max(0, Math.min(sections.length - 1, i));

  const activeIdx = () => {
    const mid = window.scrollY + window.innerHeight / 2;
    let idx = 0, best = Infinity;
    sections.forEach((s, i) => {
      const d = Math.abs(s.offsetTop + s.offsetHeight / 2 - mid);
      if (d < best) { best = d; idx = i; }
    });
    return idx;
  };

  const scrollTo = top => {
    busy = true;
    window.scrollTo({ top, behavior: 'smooth' });
    setTimeout(() => { busy = false; }, 800);
  };

  const goTo = i => scrollTo(sections[clamp(i)].offsetTop);

  const exitSnap = () => {
    const next = sections[2].nextElementSibling;
    scrollTo(next ? next.offsetTop : sections[2].offsetTop + sections[2].offsetHeight);
  };

  const step = (dir, ev) => {
    if (busy) { ev?.preventDefault(); return; }
    const thirdBottom = sections[2].offsetTop + sections[2].offsetHeight;
    if (window.scrollY >= thirdBottom - 8) return;
    const idx = activeIdx();
    ev?.preventDefault();
    if (dir > 0 && idx >= sections.length - 1) { exitSnap(); return; }
    if (dir < 0 && idx <= 0) { goTo(0); return; }
    goTo(idx + dir);
  };

  window.addEventListener('wheel', e => {
    if (Math.abs(e.deltaY) < WHEEL_MIN) return;
    step(e.deltaY > 0 ? 1 : -1, e);
  }, { passive: false });

  window.addEventListener('touchstart', e => {
    touchY = e.touches[0]?.clientY ?? 0;
  }, { passive: true });

  window.addEventListener('touchmove', e => {
    if (!touchY) return;
    const delta = touchY - (e.touches[0]?.clientY ?? touchY);
    if (Math.abs(delta) < TOUCH_MIN) return;
    step(delta > 0 ? 1 : -1, e);
    touchY = 0;
  }, { passive: false });

  window.addEventListener('keydown', e => {
    if (['ArrowDown', 'PageDown', ' '].includes(e.key)) step(1, e);
    if (['ArrowUp', 'PageUp'].includes(e.key)) step(-1, e);
  });
}

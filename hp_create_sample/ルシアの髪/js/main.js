/* ===== LUXIA HAIR — shared site script ===== */
(function () {
  var NAV = [
    { en: 'CONCEPT', ja: 'コンセプト', href: 'concept.html', key: 'concept' },
    { en: 'STYLE', ja: 'ヘアスタイル', href: 'style.html', key: 'style' },
    { en: 'SALON', ja: 'サロン一覧', href: 'salon.html', key: 'salon' },
    { en: 'MENU', ja: 'メニュー', href: 'menu.html', key: 'menu' },
    { en: 'CAMPAIGN', ja: 'キャンペーン', href: 'campaign.html', key: 'campaign' },
    { en: 'NEWS', ja: 'お知らせ', href: 'news.html', key: 'news' }
  ];

  function buildHeader(active) {
    var links = NAV.map(function (n) {
      var cls = n.key === active ? ' class="active"' : '';
      return '<a href="' + n.href + '"' + cls + '><span class="en">' + n.en + '</span><span class="ja">' + n.ja + '</span></a>';
    }).join('');
    var mlinks = NAV.map(function (n) {
      return '<a href="' + n.href + '">' + n.en + '　' + n.ja + '</a>';
    }).join('') + '<a href="reserve.html">RESERVE　ご予約</a>';
    return '' +
      '<header class="site-header">' +
        '<a class="logo" href="index.html"><img src="assets/logo.png" alt="LUXIA HAIR"></a>' +
        '<nav>' + links + '</nav>' +
        '<a class="reserve" href="reserve.html"><span class="en">RESERVE</span><span class="ja">ご予約はこちら</span></a>' +
        '<a class="burger" href="#" id="burger" aria-label="menu"><span></span><span></span><span></span><span class="lbl">MENU</span></a>' +
      '</header>' +
      '<div class="mnav" id="mnav">' + mlinks + '</div>';
  }

  function buildFooter() {
    var cols = [
      { head: 'CONCEPT', href: 'concept.html', links: [['コンセプト', 'concept.html'], ['こだわり', 'concept.html']] },
      { head: 'STYLE', href: 'style.html', links: [['ヘアスタイル', 'style.html'], ['スタイリスト', 'style.html']] },
      { head: 'SALON', href: 'salon.html', links: [['サロン一覧', 'salon.html'], ['サロンのこだわり', 'salon.html']] },
      { head: 'MENU', href: 'menu.html', links: [['メニュー', 'menu.html'], ['ヘアケア', 'menu.html']] },
      { head: 'CAMPAIGN', href: 'campaign.html', links: [['キャンペーン', 'campaign.html'], ['お知らせ', 'news.html']] },
      { head: 'CONTACT', href: 'contact.html', links: [['お問い合わせ', 'contact.html'], ['よくあるご質問', 'contact.html']] }
    ];
    var colHtml = cols.map(function (c) {
      var ls = c.links.map(function (l) { return '<a class="link" href="' + l[1] + '">' + l[0] + '</a>'; }).join('');
      return '<div class="col"><a class="head" href="' + c.href + '">' + c.head + '</a>' + ls + '</div>';
    }).join('');
    var ig = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="2.5" y="2.5" width="19" height="19" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.6" cy="6.4" r="1.1" fill="currentColor" stroke="none"/></svg>';
    var fb = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7h2.4l.4-2.8h-2.8V9.4c0-.8.2-1.4 1.4-1.4h1.5V5.5c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8v2H8.3V14h2.6v7h2.6z"/></svg>';
    var ln = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9.5"/></svg>';
    return '' +
      '<section class="cta"><div class="inner">' +
        '<div><h2>ご予約・お問い合わせ</h2><p>上質なサロン体験を、ぜひご体感ください。</p></div>' +
        '<div class="acts">' +
          '<a class="solid" href="reserve.html"><span>ご予約はこちら</span><span style="font-family:serif;">→</span></a>' +
          '<a class="ghost" href="contact.html"><span>お問い合わせ</span><span style="font-family:serif;">→</span></a>' +
        '</div>' +
      '</div></section>' +
      '<footer class="site-footer">' +
        '<div class="cols">' +
          '<a class="logo" href="index.html"><img src="assets/logo.png" alt="LUXIA HAIR"></a>' +
          colHtml +
        '</div>' +
        '<div class="social"><a href="#" aria-label="Instagram">' + ig + '</a><a href="#" aria-label="Facebook">' + fb + '</a><a href="#" aria-label="Line">' + ln + '</a></div>' +
        '<div class="copy">© LUXIA HAIR All Rights Reserved.</div>' +
      '</footer>';
  }

  function mountChrome() {
    var active = document.body.getAttribute('data-page') || '';
    var h = document.getElementById('site-header');
    if (h) h.outerHTML = buildHeader(active);
    var f = document.getElementById('site-footer');
    if (f) f.outerHTML = buildFooter();

    var burger = document.getElementById('burger');
    var mnav = document.getElementById('mnav');
    if (burger && mnav) {
      burger.addEventListener('click', function (e) { e.preventDefault(); mnav.classList.toggle('open'); });
    }
  }

  function initHero() {
    var hero = document.querySelector('.hero');
    if (!hero) return;
    var slides = hero.querySelectorAll('.slide');
    var dots = hero.querySelectorAll('.dots button');
    var i = 0, timer;
    function show(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) { s.classList.toggle('active', k === i); });
      dots.forEach(function (d, k) { d.classList.toggle('active', k === i); });
    }
    function start() { timer = setInterval(function () { show(i + 1); }, 5000); }
    function reset() { clearInterval(timer); start(); }
    var prev = hero.querySelector('.prev'), next = hero.querySelector('.next');
    if (prev) prev.addEventListener('click', function () { show(i - 1); reset(); });
    if (next) next.addEventListener('click', function () { show(i + 1); reset(); });
    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); reset(); }); });
    show(0); start();
  }

  function initForms() {
    document.querySelectorAll('form.luxia').forEach(function (form) {
      form.addEventListener('submit', function (e) {
        e.preventDefault();
        var done = form.parentElement.querySelector('.form-done');
        form.style.display = 'none';
        if (done) done.classList.add('show');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
    });
  }

  function initCats() {
    var cats = document.querySelectorAll('.cats .cat');
    if (!cats.length) return;
    cats.forEach(function (c) {
      c.addEventListener('click', function () {
        cats.forEach(function (x) { x.classList.remove('active'); });
        c.classList.add('active');
      });
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    mountChrome();
    initHero();
    initForms();
    initCats();
  });
})();

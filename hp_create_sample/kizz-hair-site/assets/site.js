const $ = (selector, scope = document) => scope.querySelector(selector);
const $$ = (selector, scope = document) => [...scope.querySelectorAll(selector)];

window.addEventListener("DOMContentLoaded", () => {
  const loader = $(".loader");
  if (loader) {
    const seen = sessionStorage.getItem("kizzLoaderSeen");
    if (seen) {
      loader.classList.add("hide");
    } else {
      sessionStorage.setItem("kizzLoaderSeen", "1");
      setTimeout(() => loader.classList.add("hide"), 1700);
    }
  }

  const hamburger = $(".hamburger");
  const mobileMenu = $(".mobile-menu");
  hamburger?.addEventListener("click", () => {
    const open = mobileMenu.classList.toggle("open");
    hamburger.setAttribute("aria-expanded", String(open));
  });
  $$(".mobile-menu a").forEach((link) => link.addEventListener("click", () => mobileMenu.classList.remove("open")));

  $$(".faq-q").forEach((button) => {
    button.addEventListener("click", () => button.closest(".faq-item").classList.toggle("open"));
  });

  const tabs = $$(".tab");
  tabs.forEach((tab) => {
    tab.addEventListener("click", () => {
      tabs.forEach((t) => t.classList.remove("active"));
      tab.classList.add("active");
      $$(".salon-panel").forEach((panel) => panel.classList.toggle("active", panel.dataset.salon === tab.dataset.salon));
    });
  });

  const filters = $$(".filter");
  filters.forEach((filter) => {
    filter.addEventListener("click", () => {
      filters.forEach((f) => f.classList.remove("active"));
      filter.classList.add("active");
      const value = filter.dataset.filter;
      $$(".style-card").forEach((card) => {
        card.style.display = value === "ALL" || card.dataset.category === value ? "" : "none";
      });
    });
  });

  $("form[data-reserve]")?.addEventListener("submit", (event) => {
    event.preventDefault();
    $(".complete")?.classList.add("show");
    event.currentTarget.reset();
  });

  initFullScreenSnap();
});

function initFullScreenSnap() {
  const snapPage = $(".page.snap");
  if (!snapPage) return;
  const sections = $$(".full-section", snapPage).slice(0, 3);
  if (sections.length < 3) return;

  let isAnimating = false;
  let touchStartY = 0;
  const wheelThreshold = 28;
  const touchThreshold = 48;

  const clampIndex = (index) => Math.max(0, Math.min(sections.length - 1, index));

  const getActiveIndex = () => {
    const viewportCenter = window.scrollY + window.innerHeight / 2;
    let active = 0;
    let closest = Infinity;
    sections.forEach((section, index) => {
      const center = section.offsetTop + section.offsetHeight / 2;
      const distance = Math.abs(center - viewportCenter);
      if (distance < closest) {
        closest = distance;
        active = index;
      }
    });
    return active;
  };

  const scrollToY = (top) => {
    isAnimating = true;
    window.scrollTo({ top, behavior: "smooth" });
    window.setTimeout(() => {
      isAnimating = false;
    }, 780);
  };

  const scrollToSection = (index) => scrollToY(sections[clampIndex(index)].offsetTop);

  const scrollAfterIntro = () => {
    const next = sections[2].nextElementSibling;
    scrollToY(next ? next.offsetTop : sections[2].offsetTop + sections[2].offsetHeight);
  };

  const handleStep = (direction, event) => {
    if (isAnimating) {
      event?.preventDefault();
      return;
    }

    const thirdBottom = sections[2].offsetTop + sections[2].offsetHeight;
    const inIntroArea = window.scrollY < thirdBottom - 8;
    if (!inIntroArea) return;

    const activeIndex = getActiveIndex();
    event?.preventDefault();

    if (direction > 0 && activeIndex >= sections.length - 1) {
      scrollAfterIntro();
      return;
    }

    if (direction < 0 && activeIndex <= 0) {
      scrollToSection(0);
      return;
    }

    scrollToSection(activeIndex + direction);
  };

  window.addEventListener("wheel", (event) => {
    if (Math.abs(event.deltaY) < wheelThreshold) return;
    handleStep(event.deltaY > 0 ? 1 : -1, event);
  }, { passive: false });

  window.addEventListener("touchstart", (event) => {
    touchStartY = event.touches[0]?.clientY ?? 0;
  }, { passive: true });

  window.addEventListener("touchmove", (event) => {
    if (!touchStartY) return;
    const currentY = event.touches[0]?.clientY ?? touchStartY;
    const delta = touchStartY - currentY;
    if (Math.abs(delta) < touchThreshold) return;
    handleStep(delta > 0 ? 1 : -1, event);
    touchStartY = 0;
  }, { passive: false });

  window.addEventListener("keydown", (event) => {
    const downKeys = ["ArrowDown", "PageDown", " "];
    const upKeys = ["ArrowUp", "PageUp"];
    if (downKeys.includes(event.key)) handleStep(1, event);
    if (upKeys.includes(event.key)) handleStep(-1, event);
  });
}

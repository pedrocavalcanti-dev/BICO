(() => {
  const carousel = document.querySelector("[data-carousel]");
  if (!carousel) return;

  const slides = Array.from(carousel.querySelectorAll("[data-slide]"));
  const dots = Array.from(carousel.querySelectorAll("[data-carousel-dot]"));
  if (slides.length < 2) return;

  let activeIndex = Math.max(0, slides.findIndex((slide) => slide.classList.contains("is-active")));
  const show = (index) => {
    activeIndex = (index + slides.length) % slides.length;
    slides.forEach((slide, itemIndex) => {
      const active = itemIndex === activeIndex;
      slide.hidden = !active;
      slide.classList.toggle("is-active", active);
    });
    dots.forEach((dot, itemIndex) => {
      if (itemIndex === activeIndex) dot.setAttribute("aria-current", "true");
      else dot.removeAttribute("aria-current");
    });
  };

  carousel.querySelector("[data-carousel-previous]")?.addEventListener("click", () => show(activeIndex - 1));
  carousel.querySelector("[data-carousel-next]")?.addEventListener("click", () => show(activeIndex + 1));
  dots.forEach((dot) => dot.addEventListener("click", () => show(Number(dot.dataset.carouselDot))));
})();

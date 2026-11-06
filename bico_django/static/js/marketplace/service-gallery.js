document.querySelectorAll("[data-service-gallery]").forEach((gallery) => {
  const cover = gallery.querySelector("[data-gallery-cover]");
  if (!cover) return;

  gallery.querySelectorAll("[data-gallery-image]").forEach((button) => {
    button.addEventListener("click", () => {
      cover.src = button.dataset.galleryImage;
      cover.alt = button.dataset.galleryAlt || "Foto do serviço";
      gallery.querySelectorAll("[data-gallery-image]").forEach((thumbnail) => {
        const selected = thumbnail === button;
        thumbnail.classList.toggle("is-active", selected);
        thumbnail.setAttribute("aria-pressed", String(selected));
      });
    });
  });
});

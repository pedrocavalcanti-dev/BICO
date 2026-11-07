(() => {
  const button = document.querySelector(".provider-menu-toggle");
  const sidebar = document.querySelector(".provider-sidebar");
  if (!button || !sidebar) return;

  const mobile = window.matchMedia("(max-width: 760px)");
  const setLabels = (expanded) => {
    button.setAttribute("aria-expanded", String(expanded));
    const label = mobile.matches
      ? expanded
        ? "Fechar navegação"
        : "Abrir navegação"
      : expanded
        ? "Recolher navegação"
        : "Expandir navegação";
    button.setAttribute("aria-label", label);
    button.setAttribute("title", label);
  };

  button.addEventListener("click", () => {
    const expanded = button.getAttribute("aria-expanded") === "true";
    if (mobile.matches) {
      sidebar.classList.toggle("is-open", !expanded);
    } else {
      document.body.classList.toggle("provider-sidebar-collapsed", expanded);
    }
    setLabels(!expanded);
  });

  mobile.addEventListener("change", () => {
    sidebar.classList.remove("is-open");
    document.body.classList.remove("provider-sidebar-collapsed");
    setLabels(!mobile.matches);
  });
  setLabels(!mobile.matches);

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && sidebar.classList.contains("is-open")) {
      sidebar.classList.remove("is-open");
      setLabels(false);
      button.focus();
    }
  });
})();

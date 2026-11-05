document.querySelectorAll("[data-password-toggle]").forEach((button) => {
  button.addEventListener("click", () => {
    const input = button.parentElement.querySelector("input");
    if (!input) return;
    const show = input.type === "password";
    input.type = show ? "text" : "password";
    button.setAttribute("aria-pressed", String(show));
    button.setAttribute("aria-label", show ? "Ocultar senha" : "Mostrar senha");
  });
});

document.querySelectorAll(".auth-form").forEach((form) => {
  form.addEventListener("submit", () => {
    const submit = form.querySelector('button[type="submit"]');
    if (!submit) return;
    submit.disabled = true;
    submit.dataset.label = submit.textContent;
    submit.textContent = "Aguarde…";
  });
});

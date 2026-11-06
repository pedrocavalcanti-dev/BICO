document.addEventListener("DOMContentLoaded", () => {
  const formatDocumentNumber = (input) => {
    const isCompany = input.name === "cnpj";
    const digits = input.value.replace(/\D/g, "").slice(0, isCompany ? 14 : 11);
    let formatted = digits;
    if (isCompany) {
      formatted = digits
        .replace(/^(\d{2})(\d)/, "$1.$2")
        .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
        .replace(/^(\d{2})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3/$4")
        .replace(/(\d{4})(\d)/, "$1-$2");
    } else {
      formatted = digits
        .replace(/^(\d{3})(\d)/, "$1.$2")
        .replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3")
        .replace(/^(\d{3})\.(\d{3})\.(\d{3})(\d)/, "$1.$2.$3-$4");
    }
    input.value = formatted;
  };
  document.querySelectorAll('[name="cpf"], [name="representative_cpf"], [name="cnpj"]').forEach((input) => {
    input.addEventListener("input", () => formatDocumentNumber(input));
  });

  document.querySelectorAll("[data-document-input]").forEach((input) => {
    input.addEventListener("change", () => {
      const preview = document.querySelector(`[data-document-preview="${input.name}"]`);
      const placeholder = document.querySelector(`[data-document-placeholder="${input.name}"]`);
      const status = input.closest(".provider-document")?.querySelector("[data-document-file-name]");
      if (!preview || !input.files?.[0]) return;
      const file = input.files[0];
      if (preview.dataset.objectUrl) URL.revokeObjectURL(preview.dataset.objectUrl);
      const objectUrl = URL.createObjectURL(file);
      preview.src = objectUrl;
      preview.dataset.objectUrl = objectUrl;
      preview.hidden = false;
      if (placeholder) placeholder.hidden = true;
      if (status) status.textContent = `${file.name} · ${(file.size / 1024 / 1024).toFixed(1)} MB`;
    });
  });

  const modes = document.querySelectorAll(".provider-service-modes input[type=checkbox]");
  const updateModeFields = () => {
    const selected = new Set([...modes].filter((item) => item.checked).map((item) => item.value));
    document.querySelectorAll("[data-field]").forEach((wrapper) => {
      const name = wrapper.dataset.field;
      const visible = name.startsWith("fixed_point_") ? selected.has("FIXED")
        : ["service_region", "service_radius_km"].includes(name) ? selected.has("HOME")
          : name === "remote_scope" ? selected.has("REMOTE") : true;
      wrapper.hidden = !visible;
      wrapper.querySelectorAll("input,select,textarea").forEach((control) => {
        control.disabled = !visible;
      });
    });
  };
  modes.forEach((mode) => mode.addEventListener("change", updateModeFields));
  if (modes.length) updateModeFields();
});

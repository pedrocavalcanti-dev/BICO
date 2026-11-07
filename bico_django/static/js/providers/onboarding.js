document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("#provider-onboarding-form");
  if (!form) return;
  const find = (selector) => form.querySelector(selector);
  const all = (selector) => [...form.querySelectorAll(selector)];
  const field = (name) => form.elements.namedItem(name);
  const step = Number(form.dataset.step);
  const csrf = field("csrfmiddlewaretoken").value;
  const saveStatus = document.querySelector("[data-save-status]");
  let timer;
  let saveQueue = Promise.resolve();
  let submitting = false;
  let uploads = 0;
  let revision = 0;
  let dirty = false;

  const setSaveStatus = (text, state = "") => {
    saveStatus.textContent = text;
    saveStatus.classList.toggle("is-saving", state === "saving");
    saveStatus.classList.toggle("is-error", state === "error");
  };
  const saveDraft = async (snapshot, version) => {
    if (submitting) return;
    setSaveStatus("Salvando…", "saving");
    try {
      const response = await fetch(form.dataset.autosaveUrl, {
        method: "PATCH", credentials: "same-origin", redirect: "error",
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
        body: JSON.stringify(snapshot),
      });
      if (!response.ok) throw new Error("save");
      if (version === revision) {
        dirty = false;
        setSaveStatus("Salvo automaticamente");
      }
    } catch {
      setSaveStatus("Continue para salvar a etapa", "error");
    }
  };
  const scheduleSave = () => {
    if (submitting || step === 5) return;
    dirty = true;
    revision += 1;
    const version = revision;
    setSaveStatus("Alterações não salvas");
    clearTimeout(timer);
    timer = setTimeout(() => {
      if (!form.checkValidity()) return;
      const snapshot = { step };
      for (const [name, value] of new FormData(form)) {
        if (value instanceof File || ["csrfmiddlewaretoken", "action"].includes(name)) continue;
        if (["categories", "service_modes"].includes(name)) {
          (snapshot[name] ??= []).push(value);
        } else snapshot[name] = value;
      }
      // Requests run in order so an older draft cannot overwrite the latest one.
      saveQueue = saveQueue.then(() => saveDraft(snapshot, version));
    }, 1000);
  };

  const formatMask = (input) => {
    const digits = input.value.replace(/\D/g, "");
    if (input.name === "cnpj") {
      input.value = digits.slice(0, 14).replace(/^(\d{2})(\d)/, "$1.$2")
        .replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3")
        .replace(/\.(\d{3})(\d)/, ".$1/$2").replace(/(\d{4})(\d)/, "$1-$2");
    } else if (input.name.includes("cpf")) {
      input.value = digits.slice(0, 11).replace(/^(\d{3})(\d)/, "$1.$2")
        .replace(/^(\d{3})\.(\d{3})(\d)/, "$1.$2.$3").replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    } else if (input.name.includes("phone")) {
      const phone = digits.slice(0, 11);
      input.value = phone.replace(/^(\d{2})(\d)/, "($1) $2")
        .replace(phone.length > 10 ? /(\d{5})(\d)/ : /(\d{4})(\d)/, "$1-$2");
    } else {
      input.value = digits.slice(0, 8).replace(/(\d{5})(\d)/, "$1-$2");
    }
  };
  all('[name="cpf"], [name="representative_cpf"], [name="cnpj"], [name$="phone"], [name="fixed_point_postal_code"]').forEach((input) => {
    formatMask(input);
    input.addEventListener("input", () => formatMask(input));
  });

  // Compact specialty choices, search without accents, and a server-matched limit.
  const specialties = all('[name="categories"]');
  const maxCategories = Number(form.dataset.maxCategories);
  const specialtyFeedback = find("[data-specialty-feedback]");
  const updateSpecialties = (changed) => {
    let selected = specialties.filter((item) => item.checked);
    if (changed?.checked && selected.length > maxCategories) {
      changed.checked = false;
      selected = specialties.filter((item) => item.checked);
      specialtyFeedback.textContent = `Selecione até ${maxCategories} especialidades. Desmarque uma para trocar.`;
    } else if (specialtyFeedback) {
      specialtyFeedback.textContent = selected.length
        ? `${selected.length} ${selected.length === 1 ? "especialidade selecionada" : "especialidades selecionadas"}.`
        : "Escolha as especialidades que melhor representam seus serviços.";
    }
    const counter = find("[data-specialty-count]");
    if (counter) counter.textContent = `${selected.length} / ${maxCategories}`;
  };
  specialties.forEach((item) => item.addEventListener("change", () => updateSpecialties(item)));
  if (specialties.length) updateSpecialties();
  const normalize = (text) => text.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
  const specialtySearch = find("[data-specialty-search]");
  const filterSpecialties = () => {
    const query = normalize(specialtySearch.value.trim());
    const options = all("[data-specialty-option]");
    options.forEach((option) => { option.hidden = !normalize(option.textContent).includes(query); });
    all(".onboarding-specialty-group").forEach((group) => {
      group.hidden = ![...group.querySelectorAll("[data-specialty-option]")].some((option) => !option.hidden);
    });
    find("[data-no-specialties]").hidden = options.some((option) => !option.hidden);
  };
  specialtySearch?.addEventListener("input", filterSpecialties);
  specialtySearch?.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.isComposing) return;
    // This search stays inside the step; implicit submit would activate Save and exit.
    event.preventDefault();
    filterSpecialties();
  });
  field("main_category")?.addEventListener("change", (event) => {
    const matching = specialties.find((item) => item.value === event.target.value);
    if (matching && !matching.checked) {
      matching.checked = true;
      updateSpecialties(matching);
      if (!matching.checked) event.target.value = "";
    }
  });
  const description = field("professional_description");
  const updateDescription = () => {
    const count = find("[data-description-count]");
    if (count) count.textContent = `${description.value.length} / 2000`;
  };
  if (description) {
    description.addEventListener("input", updateDescription);
    updateDescription();
  }

  // Modes share a single address editor. City/state are also available for remote-only work.
  const modes = all('[name="service_modes"]');
  const addressDetails = find("[data-address-details]");
  const show = (selector, visible) => {
    all(selector).forEach((element) => { element.hidden = !visible; });
  };
  const updateModes = () => {
    const selected = new Set(modes.filter((mode) => mode.checked).map((mode) => mode.value));
    const physical = selected.has("HOME") || selected.has("FIXED");
    show("[data-physical-fields], [data-address-number]", physical);
    show('[data-field="fixed_point_street"], [data-field="fixed_point_neighborhood"]', physical);
    show("[data-home-fields]", selected.has("HOME"));
    show("[data-fixed-details]", selected.has("FIXED"));
    show("[data-remote-fields]", selected.has("REMOTE"));
    addressDetails.querySelector("summary").hidden = !physical;
    addressDetails.open = !physical || Boolean(find(".onboarding-location .has-error"));
    const title = find("[data-location-title]");
    title.textContent = physical ? "Sua base de atendimento" : "De onde você atende?";
    find("[data-location-description]").textContent = physical
      ? "Comece pelo CEP. Nós ajudamos com o restante."
      : "Para o atendimento remoto, basta informar sua cidade-base e estado.";
  };
  modes.forEach((mode) => mode.addEventListener("change", updateModes));
  if (modes.length) updateModes();
  const radius = field("service_radius_km");
  const updateRadius = () => { find("[data-radius-output]").textContent = `${radius.value} km`; };
  if (radius) {
    radius.addEventListener("input", updateRadius);
    updateRadius();
  }
  const postal = field("fixed_point_postal_code");
  const postalButton = find("[data-postal-search]");
  let postalRequest = null;
  const lookupPostal = async () => {
    const code = postal.value.replace(/\D/g, "");
    const feedback = find("[data-postal-feedback]");
    const result = find("[data-address-result]");
    if (code.length !== 8) {
      feedback.textContent = "Informe os 8 números do CEP ou preencha o endereço manualmente.";
      addressDetails.open = true;
      return;
    }
    postalRequest?.abort();
    const controller = new AbortController();
    postalRequest = controller;
    const timeout = setTimeout(() => controller.abort(), 7000);
    postalButton.disabled = true;
    feedback.textContent = "Buscando seu endereço…";
    result.hidden = true;
    try {
      const response = await fetch(`https://viacep.com.br/ws/${code}/json/`, {
        signal: controller.signal, credentials: "omit", referrerPolicy: "no-referrer",
      });
      if (!response.ok) throw new Error("postal");
      const data = await response.json();
      if (data.erro || !data.localidade || !data.uf) throw new Error("postal");
      if (postal.value.replace(/\D/g, "") !== code) return;
      const values = {
        fixed_point_street: data.logradouro || "", fixed_point_neighborhood: data.bairro || "",
        city: data.localidade, state: data.uf,
      };
      for (const [name, value] of Object.entries(values)) field(name).value = value;
      if (!field("service_region").value) field("service_region").value = data.localidade;
      find("[data-address-label]").textContent = [data.logradouro, data.bairro, `${data.localidade} · ${data.uf}`].filter(Boolean).join(", ");
      result.hidden = false;
      addressDetails.open = !data.logradouro || !data.bairro;
      feedback.textContent = addressDetails.open
        ? "Cidade encontrada. Complete a rua e o bairro no endereço manual."
        : "Endereço preenchido. Confira e informe o número.";
      scheduleSave();
    } catch {
      if (postalRequest !== controller) return;
      feedback.textContent = "Não foi possível consultar este CEP. Preencha ou corrija o endereço manualmente.";
      addressDetails.open = true;
    } finally {
      clearTimeout(timeout);
      if (postalRequest === controller) postalButton.disabled = false;
    }
  };
  postalButton?.addEventListener("click", lookupPostal);
  postal?.addEventListener("change", () => {
    find("[data-address-result]").hidden = true;
    if (postal.value.replace(/\D/g, "").length === 8) lookupPostal();
  });

  // The existing authenticated API validates and encrypts uploads. Nothing is stored in the browser.
  const updateBusy = () => {
    document.querySelectorAll("[data-continue], [data-save-exit]").forEach((button) => {
      button.disabled = uploads > 0 || submitting;
    });
  };
  all("[data-document-input]").forEach((input) => {
    const card = input.closest("[data-document-card]");
    const preview = card.querySelector("[data-document-preview]");
    const placeholder = card.querySelector("[data-document-placeholder]");
    const feedback = card.querySelector("[data-document-feedback]");
    const state = card.querySelector("[data-document-state]");
    const handleFile = async () => {
      const file = input.files?.[0];
      if (!file || card.classList.contains("is-uploading")) return;
      card.classList.remove("is-error");
      input.setCustomValidity("");
      card.classList.add("is-uploading");
      uploads += 1;
      input.disabled = true;
      updateBusy();
      let objectUrl;
      try {
        if (!["image/jpeg", "image/png", "image/webp"].includes(file.type)) throw new Error("Escolha uma fotografia JPG, PNG ou WebP.");
        if (file.size > 8 * 1024 * 1024) throw new Error("A fotografia deve ter até 8 MB. Escolha uma imagem menor.");
        objectUrl = URL.createObjectURL(file);
        const dimensions = await new Promise((resolve, reject) => {
          const image = new Image();
          image.onload = () => resolve([image.naturalWidth, image.naturalHeight]);
          image.onerror = () => reject(new Error("Não foi possível ler a imagem. Escolha outra fotografia."));
          image.src = objectUrl;
        });
        const [width, height] = dimensions.sort((a, b) => b - a);
        if (width < 800 || height < 500) throw new Error("A imagem precisa ter pelo menos 800 × 500 px. Use a foto original.");
        if (width * height > 25_000_000) throw new Error("A imagem excede 25 megapixels. Reduza a resolução e tente novamente.");
        if (preview.dataset.objectUrl) URL.revokeObjectURL(preview.dataset.objectUrl);
        preview.src = objectUrl;
        preview.dataset.objectUrl = objectUrl;
        preview.hidden = false;
        placeholder.hidden = true;
        state.textContent = "Enviando…";
        feedback.textContent = "Verificando a qualidade e salvando em área privada…";
        const payload = new FormData();
        payload.append("side", input.dataset.side);
        payload.append("file", file);
        const response = await fetch(card.closest("[data-upload-url]").dataset.uploadUrl, {
          method: "POST", credentials: "same-origin", redirect: "error",
          headers: { "X-CSRFToken": csrf }, body: payload,
        });
        const data = await response.json();
        if (!response.ok) throw new Error([data.file, data.detail].flat().filter(Boolean).join(" ") || "Não foi possível salvar a foto. Tente novamente.");
        card.dataset.saved = "true";
        card.classList.add("is-saved");
        state.textContent = "Salva";
        feedback.textContent = "Imagem salva. A identidade será conferida na análise humana.";
        // The encrypted copy is persisted; do not send the same bytes again on Continue.
        input.value = "";
      } catch (error) {
        if (objectUrl && preview.dataset.objectUrl !== objectUrl) URL.revokeObjectURL(objectUrl);
        card.classList.add("is-error");
        state.textContent = "Substitua a imagem";
        const message = error instanceof TypeError || error instanceof SyntaxError
          ? "Não foi possível enviar agora. Verifique a conexão e tente novamente."
          : error.message;
        feedback.textContent = message;
        input.setCustomValidity(message);
      } finally {
        if (card.classList.contains("is-uploading")) uploads -= 1;
        card.classList.remove("is-uploading");
        input.disabled = false;
        updateBusy();
      }
    };
    input.addEventListener("change", handleFile);
    const zone = card.querySelector(".provider-document__dropzone");
    zone.addEventListener("dragover", (event) => { event.preventDefault(); card.classList.add("is-dragging"); });
    zone.addEventListener("dragleave", () => card.classList.remove("is-dragging"));
    zone.addEventListener("drop", (event) => {
      event.preventDefault();
      card.classList.remove("is-dragging");
      if (input.disabled || !event.dataTransfer.files.length) return;
      const transfer = new DataTransfer();
      transfer.items.add(event.dataTransfer.files[0]);
      input.files = transfer.files;
      handleFile();
    });
  });

  all(".provider-field-wrap").forEach((wrapper) => {
    const control = wrapper.querySelector("input, select, textarea");
    const help = wrapper.querySelector(".provider-field__help");
    if (help?.id && control) control.setAttribute("aria-describedby", help.id);
  });
  all(".has-error").forEach((wrapper) => {
    const details = wrapper.closest("details");
    if (details) details.open = true;
  });
  form.addEventListener("input", (event) => {
    if (event.target.name && event.target.type !== "file") scheduleSave();
  });
  form.addEventListener("change", (event) => {
    if (event.target.name && event.target.type !== "file") scheduleSave();
  });
  form.addEventListener("submit", async (event) => {
    if (submitting) { event.preventDefault(); return; }
    event.preventDefault();
    clearTimeout(timer);
    const submitter = event.submitter;
    const invalid = all("input, select, textarea").find((control) => !control.disabled && !control.checkValidity());
    // Saving and leaving the review does not require its submission acknowledgement.
    const needsValidation = submitter?.value !== "save_exit" || step < 5;
    if (invalid && needsValidation) {
      const details = invalid.closest("details");
      if (details) details.open = true;
      invalid.focus();
      invalid.reportValidity();
      return;
    }
    if (uploads) return;
    submitting = true;
    updateBusy();
    setSaveStatus(step === 5 && submitter?.value === "submit" ? "Enviando solicitação…" : "Salvando…", "saving");
    await saveQueue;
    // Preserve the clicked action when disabling the controls before a native POST.
    const action = document.createElement("input");
    action.type = "hidden"; action.name = "action"; action.value = submitter?.value || "continue";
    form.append(action);
    HTMLFormElement.prototype.submit.call(form);
  });
  window.addEventListener("beforeunload", (event) => {
    if (!submitting && (dirty || uploads)) { event.preventDefault(); event.returnValue = ""; }
  });
});

/**
 * Muestra un mensaje dentro de un contenedor de alerta.
 * @param {HTMLElement} container - el elemento donde va el mensaje
 * @param {string} message
 * @param {"error"|"success"} type
 */
export function showAlert(container, message, type = "error", extraClass = "") {
    container.textContent = message;
    container.className = `alert alert--${type}${extraClass ? " " + extraClass : ""}`;
    container.hidden = false;
}

export function clearAlert(container) {
    container.textContent = "";
    container.hidden = true;
}

/**
 * Muestra un mensaje de error específico bajo un campo de formulario.
 * @param {HTMLElement} fieldEl - el <input>
 * @param {HTMLElement} errorEl - el <span> de error asociado
 * @param {string|null} message - si es null, limpia el error
 */
export function setFieldError(fieldEl, errorEl, message) {
    if (message) {
        fieldEl.classList.add("is-invalid");
        errorEl.textContent = message;
    } else {
        fieldEl.classList.remove("is-invalid");
        errorEl.textContent = "";
    }
}

export function setLoading(buttonEl, loadingText = "Cargando...") {
    const originalText = buttonEl.textContent;
    buttonEl.disabled = true;
    buttonEl.textContent = loadingText;
    return () => {
        buttonEl.disabled = false;
        buttonEl.textContent = originalText;
    };
}

export function renderAccessRestricted(container, { title, message, buttonText, buttonHref }) {
    container.innerHTML = `
    <div class="access-restricted">
      <div class="access-restricted__icon" aria-hidden="true">🔒</div>
      <h2>${title}</h2>
      <p class="text-muted">${message}</p>
      <a href="${buttonHref}" class="btn btn--primary" style="margin-top: var(--space-md);">${buttonText}</a>
    </div>
  `;
    container.hidden = false;
}
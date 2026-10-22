
/**
 * Escapa caracteres especiales para evitar que el contenido dinámico
 * sea interpretado como HTML.
 *
 * @param {*} value
 * @returns {string}
 */
export function escapeHtml(value) {
    return String(value ?? "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

/**
 * Muestra un mensaje dentro de un contenedor de alerta.
 *
 * @param {HTMLElement} container
 * @param {string} message
 * @param {"error"|"success"} type
 * @param {string} extraClass
 */
export function showAlert(
    container,
    message,
    type = "error",
    extraClass = ""
) {
    if (!container) {
        return;
    }

    const allowedTypes = ["error", "success"];
    const alertType = allowedTypes.includes(type) ? type : "error";

    container.textContent = String(message ?? "");
    container.className = `alert alert--${alertType}`;

    if (extraClass) {
        container.classList.add(...extraClass.split(/\s+/).filter(Boolean));
    }

    container.hidden = false;
}

/**
 * Limpia un mensaje de alerta.
 *
 * @param {HTMLElement} container
 */
export function clearAlert(container) {
    if (!container) {
        return;
    }

    container.textContent = "";
    container.hidden = true;
}

/**
 * Muestra un mensaje de error debajo de un campo de formulario.
 *
 * @param {HTMLElement} fieldEl
 * @param {HTMLElement} errorEl
 * @param {string|null} message
 */
export function setFieldError(fieldEl, errorEl, message) {
    if (fieldEl) {
        fieldEl.classList.toggle("is-invalid", Boolean(message));
    }

    if (errorEl) {
        errorEl.textContent = message ? String(message) : "";
    }
}

/**
 * Deshabilita un botón mientras se ejecuta una operación.
 *
 * @param {HTMLButtonElement} buttonEl
 * @param {string} loadingText
 * @returns {Function}
 */
export function setLoading(
    buttonEl,
    loadingText = "Cargando..."
) {
    if (!buttonEl) {
        return () => {};
    }

    const originalText = buttonEl.textContent;
    const wasDisabled = buttonEl.disabled;

    buttonEl.disabled = true;
    buttonEl.textContent = loadingText;

    return () => {
        buttonEl.disabled = wasDisabled;
        buttonEl.textContent = originalText;
    };
}

/**
 * Muestra una pantalla de acceso restringido.
 *
 * @param {HTMLElement} container
 * @param {Object} options
 * @param {string} options.title
 * @param {string} options.message
 * @param {string} options.buttonText
 * @param {string} options.buttonHref
 */
export function renderAccessRestricted(
    container,
    {
        title,
        message,
        buttonText,
        buttonHref
    }
) {
    if (!container) {
        return;
    }

    const safeHref = escapeHtml(buttonHref ?? "index.html");

    container.innerHTML = `
        <div class="access-restricted">
            <div
                class="access-restricted__icon"
                aria-hidden="true"
            >
                🔒
            </div>

            <h2>${escapeHtml(title)}</h2>

            <p class="text-muted">
                ${escapeHtml(message)}
            </p>

            <a
                href="${safeHref}"
                class="btn btn--primary access-restricted__button"
            >
                ${escapeHtml(buttonText)}
            </a>
        </div>
    `;

    container.hidden = false;
}

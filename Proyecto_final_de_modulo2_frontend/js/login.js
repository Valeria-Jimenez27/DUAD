import { login } from "./authService.js";
import { isLoggedIn, isAdmin } from "./storage.js";
import { validateField } from "./validators.js";
import { showAlert, clearAlert, setFieldError, setLoading } from "./ui.js";

if (isLoggedIn()) {
    window.location.href = isAdmin() ? "admin-panel.html" : "catalog.html";
}

const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const emailError = document.getElementById("email-error");
const passwordError = document.getElementById("password-error");
const formAlert = document.getElementById("form-alert");
const submitBtn = document.getElementById("submit-btn");

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearAlert(formAlert);

    const emailMsg = validateField(emailInput.value, "email");
    const passwordMsg = validateField(passwordInput.value, "required");

    setFieldError(emailInput, emailError, emailMsg);
    setFieldError(passwordInput, passwordError, passwordMsg);

    if (emailMsg || passwordMsg) return;

    const restoreButton = setLoading(submitBtn, "Ingresando...");

    try {
        const result = await login({
            email: emailInput.value.trim(),
            password: passwordInput.value,
        });

        window.location.href = result.role === "admin" ? "admin-panel.html" : "catalog.html";
    } catch (error) {
        // error.message ya viene traducido desde apiFetch (config.js), nunca
        // dejamos que un error de la API se quede solo en consola.
        showAlert(formAlert, error.message, "error", "alert--plain");
    } finally {
        restoreButton();
    }
});
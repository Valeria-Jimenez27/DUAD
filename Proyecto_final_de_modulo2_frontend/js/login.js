
import { login } from "./authService.js";
import { isLoggedIn, isAdmin } from "./storage.js";
import { validateField } from "./validators.js";
import {
    showAlert,
    clearAlert,
    setFieldError,
    setLoading
} from "./ui.js";

// Si ya hay una sesión activa, redirige según el rol.
if (isLoggedIn()) {
    window.location.href = isAdmin()
        ? "admin-panel.html"
        : "catalog.html";
}

const form = document.getElementById("login-form");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const emailError = document.getElementById("email-error");
const passwordError = document.getElementById("password-error");
const formAlert = document.getElementById("form-alert");
const submitBtn = document.getElementById("submit-btn");

if (!form) {
    console.error('No se encontró el formulario con ID "login-form".');
} else {
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearAlert(formAlert);

        const emailMsg = validateField(
            emailInput.value.trim(),
            "email"
        );

        const passwordMsg = validateField(
            passwordInput.value,
            "required"
        );

        setFieldError(emailInput, emailError, emailMsg);
        setFieldError(passwordInput, passwordError, passwordMsg);

        if (emailMsg || passwordMsg) {
            showAlert(
                formAlert,
                "Por favor, revisa los campos e inténtalo de nuevo.",
                "error",
                "alert--plain"
            );
            return;
        }

        const restoreButton = setLoading(
            submitBtn,
            "Ingresando..."
        );

        try {
            const result = await login({
                email: emailInput.value.trim(),
                password: passwordInput.value
            });

            const role = result?.role;

            window.location.href =
                role === "admin" || isAdmin()
                    ? "admin-panel.html"
                    : "catalog.html";
        } catch (error) {
            showAlert(
                formAlert,
                error?.message ||
                    "No se pudo iniciar sesión. Verifica tus credenciales e inténtalo de nuevo.",
                "error",
                "alert--plain"
            );
        } finally {
            restoreButton();
        }
    });
}

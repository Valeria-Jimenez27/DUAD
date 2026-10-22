
import { register, login } from "./authService.js";
import { isLoggedIn, isAdmin } from "./storage.js";
import { validateField } from "./validators.js";
import {
    showAlert,
    clearAlert,
    setFieldError,
    setLoading
} from "./ui.js";

// Si ya existe una sesión, redirige según el rol.
if (isLoggedIn()) {
    window.location.href = isAdmin()
        ? "admin-panel.html"
        : "catalog.html";
}

const form = document.getElementById("register-form");

const fields = {
    firstName: document.getElementById("first-name"),
    lastName: document.getElementById("last-name"),
    email: document.getElementById("email"),
    password: document.getElementById("password"),
    confirmPassword: document.getElementById("confirm-password"),
    phone: document.getElementById("phone"),
    address: document.getElementById("address")
};

const errors = {
    firstName: document.getElementById("first-name-error"),
    lastName: document.getElementById("last-name-error"),
    email: document.getElementById("email-error"),
    password: document.getElementById("password-error"),
    confirmPassword: document.getElementById("confirm-password-error"),
    phone: document.getElementById("phone-error"),
    address: document.getElementById("address-error")
};

const formAlert = document.getElementById("form-alert");
const submitBtn = document.getElementById("submit-btn");

// Comprueba que la estructura HTML esperada exista.
if (!form) {
    console.error('No se encontró el formulario con ID "register-form".');
} else {
    // Valida los campos del formulario.
    function validateForm() {
        const rules = {
            firstName: "name",
            lastName: "name",
            email: "email",
            password: "password",
            phone: "phone",
            address: "required"
        };

        let isValid = true;

        for (const [key, rule] of Object.entries(rules)) {
            const field = fields[key];

            if (!field) {
                isValid = false;
                continue;
            }

            const message = validateField(field.value.trim(), rule);

            setFieldError(field, errors[key], message);

            if (message) {
                isValid = false;
            }
        }

        const password = fields.password?.value ?? "";
        const confirmPassword = fields.confirmPassword?.value ?? "";

        let confirmMessage = null;

        if (!confirmPassword) {
            confirmMessage = "Confirma tu contraseña.";
        } else if (confirmPassword !== password) {
            confirmMessage = "Las contraseñas no coinciden.";
        }

        setFieldError(
            fields.confirmPassword,
            errors.confirmPassword,
            confirmMessage
        );

        if (confirmMessage) {
            isValid = false;
        }

        return isValid;
    }

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        clearAlert(formAlert);

        if (!validateForm()) {
            showAlert(
                formAlert,
                "Por favor completa todos los campos correctamente.",
                "error",
                "alert--plain"
            );
            return;
        }

        const restoreButton = setLoading(
            submitBtn,
            "Creando cuenta..."
        );

        try {
            const email = fields.email.value.trim();

            await register({
                firstName: fields.firstName.value.trim(),
                lastName: fields.lastName.value.trim(),
                email,
                password: fields.password.value,
                phone: fields.phone.value.trim(),
                address: fields.address.value.trim()
            });

            // Inicia sesión con la cuenta recién registrada.
            await login({
                email,
                password: fields.password.value
            });

            // Los usuarios recién registrados van al catálogo.
            window.location.href = "catalog.html";
        } catch (error) {
            showAlert(
                formAlert,
                error?.message || "No se pudo crear la cuenta. Inténtalo de nuevo.",
                "error",
                "alert--plain"
            );
        } finally {
            restoreButton();
        }
    });
}

import { register, login } from "./authService.js";
import { isLoggedIn, isAdmin } from "./storage.js";
import { validateField } from "./validators.js";
import { showAlert, clearAlert, setFieldError, setLoading } from "./ui.js";

if (isLoggedIn()) {
    window.location.href = isAdmin() ? "admin-panel.html" : "catalog.html";
}

const form = document.getElementById("register-form");
const fields = {
    firstName: document.getElementById("first-name"),
    lastName: document.getElementById("last-name"),
    email: document.getElementById("email"),
    password: document.getElementById("password"),
    confirmPassword: document.getElementById("confirm-password"),
    phone: document.getElementById("phone"),
    address: document.getElementById("address"),
};
const errors = {
    firstName: document.getElementById("first-name-error"),
    lastName: document.getElementById("last-name-error"),
    email: document.getElementById("email-error"),
    password: document.getElementById("password-error"),
    confirmPassword: document.getElementById("confirm-password-error"),
    phone: document.getElementById("phone-error"),
    address: document.getElementById("address-error"),
};
const formAlert = document.getElementById("form-alert");
const submitBtn = document.getElementById("submit-btn");

function validateForm() {
    const rules = {
        firstName: "name",
        lastName: "name",
        email: "email",
        password: "password",
        phone: "phone",
        address: "required",
    };

    let isValid = true;

    for (const [key, rule] of Object.entries(rules)) {
        const message = validateField(fields[key].value, rule);
        setFieldError(fields[key], errors[key], message);
        if (message) isValid = false;
    }

    const confirmMsg =
        fields.confirmPassword.value !== fields.password.value
            ? "Las contraseñas no coinciden."
            : null;
    setFieldError(fields.confirmPassword, errors.confirmPassword, confirmMsg);
    if (confirmMsg) isValid = false;

    return isValid;
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearAlert(formAlert);

    if (!validateForm()) {
        showAlert(formAlert, "Por favor completa todos los campos correctamente.", "error", "alert--plain");
        return;
    }

    const restoreButton = setLoading(submitBtn, "Creando cuenta...");

    try {
        await register({
            firstName: fields.firstName.value.trim(),
            lastName: fields.lastName.value.trim(),
            email: fields.email.value.trim(),
            password: fields.password.value,
            phone: fields.phone.value.trim(),
            address: fields.address.value.trim(),
        });

        await login({
            email: fields.email.value.trim(),
            password: fields.password.value,
        });

        window.location.href = "catalog.html"; // un usuario recién creado siempre es "user"
    } catch (error) {
        showAlert(formAlert, error.message, "error", "alert--plain");
    } finally {
        restoreButton();
    }
});
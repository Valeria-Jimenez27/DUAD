/* ==========================================================================
   validators.js — Validaciones de formularios con Regex.
   Puras funciones: reciben un valor, devuelven true/false o un mensaje.
   No tocan el DOM.
   ========================================================================== */

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const PASSWORD_REGEX = /^(?=.*[A-Za-z])(?=.*\d).{8,}$/;
const NAME_REGEX = /^[A-Za-zÀ-ÿ\s]{2,50}$/;
const PHONE_REGEX = /^\+?\d{8,15}$/;

export function isValidEmail(value) {
    return EMAIL_REGEX.test(String(value).trim());
}

export function isValidPassword(value) {
    return PASSWORD_REGEX.test(String(value));
}

export function isValidName(value) {
    return NAME_REGEX.test(String(value).trim());
}

export function isValidPhone(value) {
    return PHONE_REGEX.test(String(value).trim());
}

export function isNotEmpty(value) {
    return String(value).trim().length > 0;
}


export function validateField(value, rule) {
    switch (rule) {
        case "email":
            return isValidEmail(value) ? null : "Ingresa un correo válido (ej. nombre@dominio.com).";
        case "password":
            return isValidPassword(value)
                ? null
                : "La contraseña debe tener mínimo 8 caracteres, con al menos una letra y un número.";
        case "name":
            return isValidName(value) ? null : "Ingresa un nombre de 2 a 50 caracteres, usando solo letras y espacios.";
        case "phone":
            return isValidPhone(value) ? null : "Ingresa un teléfono válido (8 a 15 dígitos).";
        case "required":
            return isNotEmpty(value) ? null : "Este campo es obligatorio.";
        default:
            return null;
    }
}
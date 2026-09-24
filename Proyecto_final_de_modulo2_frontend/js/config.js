export const API_BASE_URL = "http://127.0.0.1:5000";

// 🔧 MODO DEMO: en true, ninguna página llama a la API real — todo se
// simula en memoria (js/mockData.js).
// todo vuelve a hablar con la API real sin tocar nada más.
export const USE_MOCK_DATA = true;

import { getToken } from "./storage.js";

/**
 * apiFetch — wrapper único sobre fetch para toda la app.
 * Centraliza: headers, token, parseo de errores del backend
 * @param {string} path 
 * @param {object} options 
 * @returns {Promise<any>}
 * @throws {ApiError}
 */
export async function apiFetch(path, { method = "GET", body, requiresAuth = true } = {}) {
    const headers = { "Content-Type": "application/json" };

    if (requiresAuth) {
        const token = getToken();
        if (token) headers["Authorization"] = `Bearer ${token}`;
    }

    let response;
    try {
        response = await fetch(`${API_BASE_URL}${path}`, {
            method,
            headers,
            body: body ? JSON.stringify(body) : undefined,
        });
    } catch (networkError) {
        throw new ApiError("No se pudo conectar con el servidor. Intenta de nuevo.", 0);
    }

    let data = null;
    try {
        data = await response.json();
    } catch {
    }

    if (!response.ok) {
        const message = data?.error || "Ocurrió un error inesperado.";
        throw new ApiError(message, response.status);
    }

    return data;
}

export class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.name = "ApiError";
        this.status = status;
    }
}
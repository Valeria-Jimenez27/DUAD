
import { getToken } from "./storage.js";

export const API_BASE_URL = "http://127.0.0.1:5000";
export const USE_MOCK_DATA = false;

export class ApiError extends Error {
    constructor(message, status) {
        super(message);
        this.name = "ApiError";
        this.status = status;
    }
}

export async function apiFetch(
    path,
    {
        method = "GET",
        body,
        requiresAuth = true,
    } = {}
) {
    const headers = {
        Accept: "application/json",
    };

    if (body !== undefined) {
        headers["Content-Type"] = "application/json";
    }

    if (requiresAuth) {
        const token = getToken();

        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }
    }

    let response;

    try {
        response = await fetch(`${API_BASE_URL}${path}`, {
            method,
            headers,
            body: body !== undefined ? JSON.stringify(body) : undefined,
        });
    } catch {
        throw new ApiError(
            "No se pudo conectar con el servidor. Verifica que el backend esté ejecutándose.",
            0
        );
    }

    let data = null;

    try {
        data = await response.json();
    } catch {
        // La respuesta puede no contener JSON.
    }

    if (!response.ok) {
        const message =
            data?.error ||
            data?.message ||
            `Ocurrió un error al comunicarse con el servidor (${response.status}).`;

        throw new ApiError(message, response.status);
    }

    return data;
}

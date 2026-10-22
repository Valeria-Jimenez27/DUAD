
import { apiFetch, USE_MOCK_DATA } from "./config.js";

import {
    mockGetProducts,
    mockGetProductById,
    mockGetBrands,
    mockGetCategories,
} from "./mockData.js";

/**
 * Trae el catálogo completo.
 *
 * Si USE_MOCK_DATA es true, utiliza los datos de prueba.
 *
 * @returns {Promise<Array>}
 */
export async function getProducts() {
    if (USE_MOCK_DATA) {
        return mockGetProducts();
    }

    return apiFetch("/products");
}

/**
 * Trae un producto por su ID.
 *
 * @param {number|string} id
 * @returns {Promise<Object|null>}
 */
export async function getProductById(id) {
    if (id === null || id === undefined || String(id).trim() === "") {
        throw new Error("Debes proporcionar el ID de un producto.");
    }

    if (USE_MOCK_DATA) {
        return mockGetProductById(id);
    }

    return apiFetch(`/products/${encodeURIComponent(id)}`);
}

/**
 * Trae las marcas disponibles.
 *
 * @returns {Promise<Array>}
 */
export async function getBrands() {
    if (USE_MOCK_DATA) {
        return mockGetBrands();
    }

    return apiFetch("/brands", {
        requiresAuth: false,
    });
}

/**
 * Trae las categorías disponibles.
 *
 * @returns {Promise<Array>}
 */
export async function getCategories() {
    if (USE_MOCK_DATA) {
        return mockGetCategories();
    }

    return apiFetch("/categories", {
        requiresAuth: false,
    });
}

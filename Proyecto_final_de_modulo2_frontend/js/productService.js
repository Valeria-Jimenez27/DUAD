import { apiFetch, USE_MOCK_DATA } from "./config.js";

import {
    mockGetProducts,
    mockGetProductById,
    mockGetBrands,
    mockGetCategories
} from "./mockData.js";

/**
 * Trae el catálogo completo.
 *
 * Cuando USE_MOCK_DATA es true, utiliza los productos
 * guardados en mockData.js / localStorage.
 *
 * @returns {Promise<Array>}
 */
export async function getProducts() {
    if (USE_MOCK_DATA) {
        return mockGetProducts();
    }

    return apiFetch("/products", {
        method: "GET"
    });
}

/**
 * Trae un producto por su ID.
 *
 * @param {number|string} id
 * @returns {Promise<Object|null>}
 */
export async function getProductById(id) {
    if (USE_MOCK_DATA) {
        return mockGetProductById(id);
    }

    return apiFetch(`/products/${id}`, {
        method: "GET"
    });
}

/**
 * Trae las marcas.
 *
 * @returns {Promise<Array>}
 */
export async function getBrands() {
    if (USE_MOCK_DATA) {
        return mockGetBrands();
    }

    return apiFetch("/brands", {
        method: "GET",
        requiresAuth: false
    });
}

/**
 * Trae las categorías.
 *
 * @returns {Promise<Array>}
 */
export async function getCategories() {
    if (USE_MOCK_DATA) {
        return mockGetCategories();
    }

    return apiFetch("/categories", {
        method: "GET",
        requiresAuth: false
    });
}
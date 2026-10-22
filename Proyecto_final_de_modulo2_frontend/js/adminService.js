
import { apiFetch, USE_MOCK_DATA } from "./config.js";

import {
    mockCreateProduct,
    mockUpdateProduct,
    mockDeleteProduct,
    mockGetOrders,
    mockRefundOrder
} from "./mockData.js";

/**
 * Valida que un identificador sea un entero positivo.
 */
function validateId(id, description = "identificador") {
    const numericId = Number(id);

    if (!Number.isInteger(numericId) || numericId <= 0) {
        throw new Error(`El ${description} no es válido.`);
    }

    return numericId;
}

/**
 * Crea un producto.
 */
export async function createProduct({
    name,
    price,
    quantity,
    brandId,
    categoryId
}) {
    if (!String(name ?? "").trim()) {
        throw new Error("Ingresa el nombre del producto.");
    }

    if (!Number.isFinite(Number(price)) || Number(price) <= 0) {
        throw new Error("El precio debe ser mayor que cero.");
    }

    if (!Number.isInteger(Number(quantity)) || Number(quantity) < 0) {
        throw new Error("La cantidad debe ser un entero igual o mayor que cero.");
    }

    const productData = {
        name: String(name).trim(),
        price: Number(price),
        quantity: Number(quantity),
        brandId: validateId(brandId, "identificador de marca"),
        categoryId: validateId(categoryId, "identificador de categoría")
    };

    if (USE_MOCK_DATA) {
        return mockCreateProduct(productData);
    }

    return apiFetch("/products", {
        method: "POST",
        body: {
            name: productData.name,
            price: productData.price,
            quantity: productData.quantity,
            brand_id: productData.brandId,
            category_id: productData.categoryId
        }
    });
}

/**
 * Actualiza un producto existente.
 */
export async function updateProduct(
    id,
    {
        name,
        price,
        quantity,
        brandId,
        categoryId
    }
) {
    const productId = validateId(id, "identificador del producto");

    if (!String(name ?? "").trim()) {
        throw new Error("Ingresa el nombre del producto.");
    }

    if (!Number.isFinite(Number(price)) || Number(price) <= 0) {
        throw new Error("El precio debe ser mayor que cero.");
    }

    if (!Number.isInteger(Number(quantity)) || Number(quantity) < 0) {
        throw new Error("La cantidad debe ser un entero igual o mayor que cero.");
    }

    const productData = {
        name: String(name).trim(),
        price: Number(price),
        quantity: Number(quantity),
        brandId: validateId(brandId, "identificador de marca"),
        categoryId: validateId(categoryId, "identificador de categoría")
    };

    if (USE_MOCK_DATA) {
        return mockUpdateProduct(productId, productData);
    }

    return apiFetch(`/products/${productId}`, {
        method: "PUT",
        body: {
            name: productData.name,
            price: productData.price,
            quantity: productData.quantity,
            brand_id: productData.brandId,
            category_id: productData.categoryId
        }
    });
}

/**
 * Elimina un producto.
 */
export async function deleteProduct(id) {
    const productId = validateId(id, "identificador del producto");

    if (USE_MOCK_DATA) {
        return mockDeleteProduct(productId);
    }

    return apiFetch(`/products/${productId}`, {
        method: "DELETE"
    });
}

/**
 * Obtiene los pedidos.
 */
export async function getOrders() {
    if (USE_MOCK_DATA) {
        return mockGetOrders();
    }

    return apiFetch("/orders", {
        method: "GET"
    });
}

/**
 * Solicita el reembolso de un pedido.
 */
export async function refundOrder(orderId) {
    const numericOrderId = validateId(
        orderId,
        "identificador del pedido"
    );

    if (USE_MOCK_DATA) {
        return mockRefundOrder(numericOrderId);
    }

    return apiFetch(`/orders/${numericOrderId}/refund`, {
        method: "POST"
    });
}

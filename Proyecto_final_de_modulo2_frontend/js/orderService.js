
import { apiFetch, USE_MOCK_DATA } from "./config.js";
import {
    getCartId,
    saveCartId,
    getCustomerId,
} from "./storage.js";

import {
    mockAddItemToCart,
    mockGetCart,
    mockRemoveItemFromCart,
    mockCheckout,
    mockGetInvoice,
} from "./mockData.js";

/**
 * Obtiene el carrito existente o crea uno nuevo para el cliente.
 *
 * @returns {Promise<number|string>}
 */
export async function getOrCreateCart() {
    if (USE_MOCK_DATA) {
        saveCartId(1);
        return 1;
    }

    const existingCartId = getCartId();

    if (existingCartId) {
        return existingCartId;
    }

    const customerId = getCustomerId();

    if (!customerId || !Number.isInteger(Number(customerId))) {
        throw new Error(
            "No se encontró el identificador del cliente. Inicia sesión nuevamente."
        );
    }

    const result = await apiFetch("/carts", {
        method: "POST",
        body: {
            customer_id: Number(customerId),
        },
    });

    if (result?.cart_id === null || result?.cart_id === undefined) {
        throw new Error(
            "El servidor no devolvió el identificador del carrito."
        );
    }

    saveCartId(result.cart_id);

    return result.cart_id;
}

/**
 * Obtiene los artículos de un carrito.
 *
 * @param {number|string} cartId
 */
export async function getCart(cartId) {
    if (USE_MOCK_DATA) {
        return mockGetCart();
    }

    if (!cartId) {
        throw new Error("No se encontró el identificador del carrito.");
    }

    return apiFetch(`/carts/${encodeURIComponent(cartId)}`);
}

/**
 * Agrega un producto al carrito.
 *
 * @param {number|string} productId
 * @param {number} quantity
 */
export async function addItemToCart(productId, quantity) {
    if (
        !Number.isInteger(Number(productId)) ||
        Number(productId) <= 0
    ) {
        throw new Error("El producto seleccionado no es válido.");
    }

    if (!Number.isInteger(Number(quantity)) || Number(quantity) <= 0) {
        throw new Error("La cantidad debe ser un número entero mayor que cero.");
    }

    if (USE_MOCK_DATA) {
        return mockAddItemToCart(Number(productId), Number(quantity));
    }

    const cartId = await getOrCreateCart();

    return apiFetch(`/carts/${encodeURIComponent(cartId)}/items`, {
        method: "POST",
        body: {
            product_id: Number(productId),
            quantity: Number(quantity),
        },
    });
}

/**
 * Elimina un artículo del carrito.
 *
 * @param {number|string} cartId
 * @param {number|string} cartItemId
 */
export async function removeItemFromCart(cartId, cartItemId) {
    if (USE_MOCK_DATA) {
        return mockRemoveItemFromCart(cartItemId);
    }

    if (!cartId || !cartItemId) {
        throw new Error(
            "No se pudo identificar el artículo que deseas eliminar."
        );
    }

    return apiFetch(
        `/carts/${encodeURIComponent(cartId)}/items/${encodeURIComponent(cartItemId)}`,
        { method: "DELETE" }
    );
}

/**
 * Finaliza la compra de un carrito.
 *
 * @param {number|string} cartId
 * @param {{billingAddress: string, paymentMethod: string}} options
 */
export async function checkout(
    cartId,
    { billingAddress, paymentMethod }
) {
    if (!billingAddress?.trim()) {
        throw new Error("Ingresa la dirección de facturación.");
    }

    if (!paymentMethod) {
        throw new Error("Selecciona un método de pago.");
    }

    if (USE_MOCK_DATA) {
        return mockCheckout({
            billingAddress,
            paymentMethod,
        });
    }

    if (!cartId) {
        throw new Error("No se encontró el carrito que deseas comprar.");
    }

    return apiFetch(
        `/carts/${encodeURIComponent(cartId)}/checkout`,
        {
            method: "POST",
            body: {
                billing_address: billingAddress.trim(),
                payment_method: paymentMethod,
            },
        }
    );
}

/**
 * Obtiene la factura asociada a una orden.
 *
 * @param {number|string} orderId
 */
export async function getInvoice(orderId) {
    if (!orderId) {
        throw new Error("No se encontró el identificador de la orden.");
    }

    if (USE_MOCK_DATA) {
        return mockGetInvoice(orderId);
    }

    const result = await apiFetch(
        `/orders/${encodeURIComponent(orderId)}/invoice`
    );

    return result?.invoice ?? result;
}

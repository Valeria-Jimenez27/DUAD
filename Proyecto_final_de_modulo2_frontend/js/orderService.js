import { apiFetch, USE_MOCK_DATA } from "./config.js";
import { getCartId, saveCartId, getCustomerId } from "./storage.js";
import {
    mockAddItemToCart,
    mockGetCart,
    mockRemoveItemFromCart,
    mockCheckout,
    mockGetInvoice,
} from "./mockData.js";

export async function getOrCreateCart() {
    if (USE_MOCK_DATA) {
        saveCartId(1); // un solo carrito simulado por sesión de navegador
        return 1;
    }

    const existingCartId = getCartId();
    if (existingCartId) return existingCartId;

    const customerId = getCustomerId();
    const result = await apiFetch("/carts", {
        method: "POST",
        body: { customer_id: Number(customerId) },
    });

    saveCartId(result.cart_id);
    return result.cart_id;
}

export async function getCart(cartId) {
    if (USE_MOCK_DATA) return mockGetCart();
    return apiFetch(`/carts/${cartId}`, { method: "GET" });
}

export async function addItemToCart(productId, quantity) {
    const cartId = await getOrCreateCart();
    if (USE_MOCK_DATA) return mockAddItemToCart(productId, quantity);
    return apiFetch(`/carts/${cartId}/items`, {
        method: "POST",
        body: { product_id: productId, quantity },
    });
}

export async function removeItemFromCart(cartId, cartItemId) {
    if (USE_MOCK_DATA) return mockRemoveItemFromCart(cartItemId);
    return apiFetch(`/carts/${cartId}/items/${cartItemId}`, { method: "DELETE" });
}

export async function checkout(cartId, { billingAddress, paymentMethod }) {
    if (USE_MOCK_DATA) return mockCheckout({ billingAddress, paymentMethod });
    return apiFetch(`/carts/${cartId}/checkout`, {
        method: "POST",
        body: { billing_address: billingAddress, payment_method: paymentMethod },
    });
}

export async function getInvoice(orderId) {
    if (USE_MOCK_DATA) return mockGetInvoice(orderId);
    const result = await apiFetch(`/orders/${orderId}/invoice`, { method: "GET" });
    return result.invoice;
}
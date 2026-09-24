const KEYS = {
    TOKEN: "petstore_token",
    ROLE: "petstore_role",
    USER_NAME: "petstore_user_name",
    CUSTOMER_ID: "petstore_customer_id",
    CART_ID: "petstore_cart_id",
};

/* ---------- Sesión ---------- */

export function saveSession({ token, role, name, customerId }) {
    localStorage.setItem(KEYS.TOKEN, token);
    localStorage.setItem(KEYS.ROLE, role);
    if (name) localStorage.setItem(KEYS.USER_NAME, name);
    if (customerId) localStorage.setItem(KEYS.CUSTOMER_ID, String(customerId));
}

export function getToken() {
    return localStorage.getItem(KEYS.TOKEN);
}

export function getRole() {
    return localStorage.getItem(KEYS.ROLE);
}

export function getUserName() {
    return localStorage.getItem(KEYS.USER_NAME);
}

export function getCustomerId() {
    return localStorage.getItem(KEYS.CUSTOMER_ID);
}

export function isLoggedIn() {
    return Boolean(getToken());
}

export function isAdmin() {
    return getRole() === "admin";
}

export function clearSession() {
    Object.values(KEYS).forEach((key) => localStorage.removeItem(key));
}

/* ---------- Carrito ---------- */
export function saveCartId(cartId) {
    localStorage.setItem(KEYS.CART_ID, String(cartId));
}

export function getCartId() {
    return localStorage.getItem(KEYS.CART_ID);
}

export function clearCartId() {
    localStorage.removeItem(KEYS.CART_ID);
}
/* ---------- Carrito demo (localStorage) ---------- */
const MOCK_CART_ITEMS_KEY = "petstore_mock_cart_items";

export function getLocalCartItems() {
    try {
        const raw = localStorage.getItem(MOCK_CART_ITEMS_KEY);
        const items = raw ? JSON.parse(raw) : [];
        return Array.isArray(items) ? items : [];
    } catch {
        return [];
    }
}

export function saveLocalCartItems(items) {
    localStorage.setItem(MOCK_CART_ITEMS_KEY, JSON.stringify(items));
}

export function clearLocalCartItems() {
    localStorage.removeItem(MOCK_CART_ITEMS_KEY);
}

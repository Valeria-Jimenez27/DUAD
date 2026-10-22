
const KEYS = {
    TOKEN: "petstore_token",
    ROLE: "petstore_role",
    USER_NAME: "petstore_user_name",
    CUSTOMER_ID: "petstore_customer_id",
    CART_ID: "petstore_cart_id",
};

const MOCK_CART_ITEMS_KEY = "petstore_mock_cart_items";

/* =========================================================
   SESIÓN
   ========================================================= */

export function saveSession({ token, role, name, customerId }) {
    // Evita conservar datos de una sesión anterior.
    localStorage.removeItem(KEYS.USER_NAME);
    localStorage.removeItem(KEYS.CUSTOMER_ID);

    if (token) {
        localStorage.setItem(KEYS.TOKEN, token);
    } else {
        localStorage.removeItem(KEYS.TOKEN);
    }

    if (role) {
        localStorage.setItem(KEYS.ROLE, role);
    } else {
        localStorage.removeItem(KEYS.ROLE);
    }

    if (name) {
        localStorage.setItem(KEYS.USER_NAME, name);
    }

    if (customerId !== null && customerId !== undefined) {
        localStorage.setItem(
            KEYS.CUSTOMER_ID,
            String(customerId)
        );
    }
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
    Object.values(KEYS).forEach((key) => {
        localStorage.removeItem(key);
    });

    // Limpia también los artículos del carrito del modo demo.
    clearLocalCartItems();
}

/* =========================================================
   CARRITO REAL
   ========================================================= */

export function saveCartId(cartId) {
    if (cartId === null || cartId === undefined) {
        clearCartId();
        return;
    }

    localStorage.setItem(KEYS.CART_ID, String(cartId));
}

export function getCartId() {
    return localStorage.getItem(KEYS.CART_ID);
}

export function clearCartId() {
    localStorage.removeItem(KEYS.CART_ID);
}

/* =========================================================
   CARRITO DEMO / MOCK
   ========================================================= */

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
    if (!Array.isArray(items)) {
        throw new TypeError(
            "Los artículos del carrito deben estar en un arreglo."
        );
    }

    localStorage.setItem(
        MOCK_CART_ITEMS_KEY,
        JSON.stringify(items)
    );
}

export function clearLocalCartItems() {
    localStorage.removeItem(MOCK_CART_ITEMS_KEY);
}

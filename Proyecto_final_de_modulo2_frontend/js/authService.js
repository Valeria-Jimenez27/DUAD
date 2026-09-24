import { apiFetch, USE_MOCK_DATA } from "./config.js";
import { saveSession } from "./storage.js";
import { mockRegister, mockLogin } from "./mockData.js";

export async function register({ firstName, lastName, email, password, phone, address }) {
    if (USE_MOCK_DATA) return mockRegister({ firstName, lastName, email, password, phone, address });

    // 1) Cuenta de acceso (User) — la que permite iniciar sesión
    const userResult = await apiFetch("/register", {
        method: "POST",
        requiresAuth: false,
        body: {
            name: `${firstName} ${lastName}`,
            email,
            password,
        },
    });

    // 2) Perfil de cliente (Customer) — el que compra y tiene pedidos
    const customerResult = await apiFetch("/customers", {
        method: "POST",
        requiresAuth: false,
        body: {
            first_name: firstName,
            last_name: lastName,
            email,
            phone,
            address,
        },
    });

    return {
        userId: userResult.id,
        customerId: customerResult.customer_id,
    };
}


export async function login({ email, password }) {
    const result = USE_MOCK_DATA
        ? await mockLogin({ email })
        : await apiFetch("/login", {
            method: "POST",
            requiresAuth: false,
            body: { email, password },
        });

    saveSession({
        token: result.token,
        role: result.role,
        name: email,
        customerId: result.customer_id,
    });

    return result;
}
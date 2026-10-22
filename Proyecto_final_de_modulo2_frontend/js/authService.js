
import { apiFetch, USE_MOCK_DATA } from "./config.js";
import { saveSession } from "./storage.js";
import { mockRegister, mockLogin } from "./mockData.js";

export async function register({
    firstName,
    lastName,
    email,
    password,
    phone,
    address,
}) {
    if (USE_MOCK_DATA) {
        return mockRegister({
            firstName,
            lastName,
            email,
            password,
            phone,
            address,
        });
    }

    const result = await apiFetch("/register", {
        method: "POST",
        requiresAuth: false,
        body: {
            first_name: firstName,
            last_name: lastName,
            email,
            password,
            phone,
            address,
        },
    });

    return {
        userId: result.id,
        customerId: result.customer_id,
    };
}

export async function login({ email, password }) {
    const result = USE_MOCK_DATA
        ? await mockLogin({ email })
        : await apiFetch("/login", {
              method: "POST",
              requiresAuth: false,
              body: {
                  email,
                  password,
              },
          });

    const userName =
        result.name ??
        result.first_name ??
        result.user?.name ??
        email;

    const customerId =
        result.customer_id ??
        result.customer?.customer_id ??
        null;

    saveSession({
        token: result.token,
        role: result.role ?? result.user?.role,
        name: userName,
        customerId,
    });

    return result;
}

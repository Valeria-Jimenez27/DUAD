import {
    isLoggedIn,
    isAdmin,
    getUserName,
    clearSession,
    getCartId
} from "./storage.js";

import { getCart } from "./orderService.js";

/* =========================================================
   CONTADOR DEL CARRITO
   ========================================================= */

async function updateCartCount() {
    const cartCountEls =
        document.querySelectorAll(".cart-count");

    const cartLinks =
        document.querySelectorAll(".cart-link");

    /* Si no hay sesión, ocultamos el carrito */
    if (!isLoggedIn()) {
        cartCountEls.forEach((element) => {
            element.textContent = "0";
            element.hidden = true;
        });

        cartLinks.forEach((link) => {
            link.hidden = true;
        });

        return;
    }

    let count = 0;

    try {
        const cartId = getCartId();

        /*
         * Si el usuario todavía no tiene carrito,
         * no necesitamos crear uno solamente para
         * mostrar el contador.
         */
        if (cartId) {
            const cart = await getCart(cartId);

            count = (cart.items || []).reduce(
                (total, item) =>
                    total + Number(item.quantity || 0),
                0
            );
        }
    } catch (error) {
        console.error(
            "No se pudo actualizar el contador del carrito:",
            error
        );

        count = 0;
    }

    /*
     * Evitamos que una respuesta de la API que llegó
     * tarde vuelva a mostrar el carrito después de cerrar sesión.
     */
    if (!isLoggedIn()) {
        cartCountEls.forEach((element) => {
            element.textContent = "0";
            element.hidden = true;
        });

        cartLinks.forEach((link) => {
            link.hidden = true;
        });

        return;
    }

    cartCountEls.forEach((element) => {
        element.textContent = count;
        element.hidden = count === 0;
    });

    cartLinks.forEach((link) => {
        link.hidden = false;
    });
}


/* =========================================================
   ENCABEZADO
   ========================================================= */

function initHeader() {
    const statusEl =
        document.getElementById("user-status");

    const authLinksEl =
        document.getElementById("auth-links");

    const navEl =
        document.getElementById("site-nav");

    if (!statusEl || !authLinksEl) {
        return;
    }

    /* Actualizar contador inicial */
    updateCartCount();

    /*
     * Escuchar cambios del carrito.
     *
     * Este evento se dispara cuando se agrega,
     * elimina o modifica un producto del carrito.
     */
    window.addEventListener(
        "cart-updated",
        updateCartCount
    );

    /*
     * Mantener compatibilidad con cambios de
     * localStorage producidos por otras partes
     * de la aplicación.
     */
    window.addEventListener(
        "storage",
        updateCartCount
    );


    /* =====================================================
       USUARIO AUTENTICADO
       ===================================================== */

    if (isLoggedIn()) {
        statusEl.textContent =
            `Usuario: ${getUserName() || "Cliente"}`;

        authLinksEl.innerHTML = `
            <a
                href="#"
                id="logout-link"
                class="logout-link"
            >
                Cerrar sesión
            </a>
        `;

        const logoutLink =
            document.getElementById("logout-link");

        logoutLink.addEventListener(
            "click",
            (event) => {
                event.preventDefault();

                clearSession();

                /*
                 * Eliminar inmediatamente el carrito
                 * visual del encabezado.
                 */
                updateCartCount();

                window.location.href =
                    "index.html";
            }
        );


        /* =================================================
           ADMINISTRADOR
           ================================================= */

        if (isAdmin() && navEl) {
            const existingAdminLink =
                navEl.querySelector(
                    'a[href="admin-panel.html"]'
                );

            if (!existingAdminLink) {
                const adminLink =
                    document.createElement("a");

                adminLink.href =
                    "admin-panel.html";

                adminLink.textContent =
                    "Panel admin";

                navEl.appendChild(adminLink);
            }
        }

    } else {

        /* =================================================
           INVITADO
           ================================================= */

        statusEl.textContent =
            "Usuario: Invitado";

        authLinksEl.innerHTML = `
            <a
                href="login.html"
                class="btn btn--primary"
            >
                Iniciar sesión
            </a>
        `;

        /*
         * Asegurarnos nuevamente de que
         * el carrito no aparezca para invitados.
         */
        updateCartCount();
    }
}


/* =========================================================
   BUSCADOR DEL ENCABEZADO
   ========================================================= */

function initHeaderSearch() {
    const headerSearch =
        document.getElementById("header-search");

    if (!headerSearch) {
        return;
    }

    headerSearch.addEventListener(
        "keydown",
        (event) => {
            if (event.key !== "Enter") {
                return;
            }

            event.preventDefault();

            const query =
                headerSearch.value.trim();

            const params =
                new URLSearchParams();

            if (query) {
                params.set("search", query);
            }

            const queryString =
                params.toString();

            window.location.href =
                queryString
                    ? `catalog.html?${queryString}`
                    : "catalog.html";
        }
    );
}


/* =========================================================
   INICIO
   ========================================================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {
        initHeader();
        initHeaderSearch();
    }
);
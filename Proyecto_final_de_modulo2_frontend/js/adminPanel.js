import { getProducts } from "./productService.js";

import {
    deleteProduct,
    getOrders,
    refundOrder
} from "./adminService.js";

import {
    isLoggedIn,
    isAdmin
} from "./storage.js";

import {
    showAlert,
    renderAccessRestricted
} from "./ui.js";


const apiErrorEl = document.getElementById("api-error");
const pageContentEl = document.getElementById("page-content");
const accessRestrictedEl = document.getElementById("access-restricted");

let hasAccess = true;


/* ---------- Control de acceso ---------- */

if (!isLoggedIn()) {
    hasAccess = false;

    if (pageContentEl) {
        pageContentEl.hidden = true;
    }

    renderAccessRestricted(accessRestrictedEl, {
        title: "Debes iniciar sesión para continuar",
        message:
            "Inicia sesión con una cuenta de administrador para gestionar la tienda.",
        buttonText: "Ir a iniciar sesión",
        buttonHref: "login.html",
    });

} else if (!isAdmin()) {
    hasAccess = false;

    if (pageContentEl) {
        pageContentEl.hidden = true;
    }

    renderAccessRestricted(accessRestrictedEl, {
        title: "No tienes permisos de administrador",
        message:
            "Esta sección es exclusiva para cuentas de administrador de la tienda.",
        buttonText: "Volver al catálogo",
        buttonHref: "catalog.html",
    });
}


/* ---------- Tabs ---------- */

const tabButtons = document.querySelectorAll(".tab-btn");
const tabInventory = document.getElementById("tab-inventory");
const tabSales = document.getElementById("tab-sales");

tabButtons.forEach((btn) => {
    btn.addEventListener("click", () => {

        tabButtons.forEach((button) => {
            button.classList.remove("is-active");
        });

        btn.classList.add("is-active");

        const isInventory = btn.dataset.tab === "inventory";

        if (tabInventory) {
            tabInventory.hidden = !isInventory;
        }

        if (tabSales) {
            tabSales.hidden = isInventory;
        }
    });
});


/* ---------- Inventario ---------- */

const inventoryLoadingEl =
    document.getElementById("inventory-loading");

const inventoryTableEl =
    document.getElementById("inventory-table");

const inventoryBodyEl =
    document.getElementById("inventory-body");


async function loadInventory() {
    if (!inventoryBodyEl) return;

    try {

        if (inventoryLoadingEl) {
            inventoryLoadingEl.hidden = false;
        }

        if (inventoryTableEl) {
            inventoryTableEl.hidden = true;
        }

        const products = await getProducts();

        if (!products || products.length === 0) {

            inventoryBodyEl.innerHTML = `
                <tr>
                    <td colspan="6">
                        No hay productos registrados.
                    </td>
                </tr>
            `;

            if (inventoryLoadingEl) {
                inventoryLoadingEl.hidden = true;
            }

            if (inventoryTableEl) {
                inventoryTableEl.hidden = false;
            }

            return;
        }

        inventoryBodyEl.innerHTML = products
            .map((product) => {

                const stock = Number(product.quantity || 0);
                const price = Number(product.price || 0);

                return `
                    <tr>
                        <td>
                            ${product.name}
                        </td>

                        <td>
                            ${product.brand || "—"}
                        </td>

                        <td>
                            ${product.category || "—"}
                        </td>

                        <td>
                            $${price.toFixed(2)}
                        </td>

                        <td>
                            ${stock}
                        </td>

                        <td>
                            <a
                                href="edit-product.html?id=${product.product_id}"
                                class="btn btn--outline"
                            >
                                Editar
                            </a>

                            <button
                                type="button"
                                class="btn btn--outline"
                                data-delete-id="${product.product_id}"
                            >
                                Eliminar
                            </button>
                        </td>
                    </tr>
                `;
            })
            .join("");

        if (inventoryLoadingEl) {
            inventoryLoadingEl.hidden = true;
        }

        if (inventoryTableEl) {
            inventoryTableEl.hidden = false;
        }

    } catch (error) {

        if (inventoryLoadingEl) {
            inventoryLoadingEl.hidden = true;
        }

        showAlert(
            apiErrorEl,
            error.message || "No se pudo cargar el inventario.",
            "error"
        );
    }
}


/* ---------- Eliminar producto ---------- */

if (inventoryBodyEl) {

    inventoryBodyEl.addEventListener("click", async (event) => {

        const button = event.target.closest("[data-delete-id]");

        if (!button) return;

        const confirmed = window.confirm(
            "¿Eliminar este producto del catálogo? Esta acción no se puede deshacer."
        );

        if (!confirmed) return;

        try {

            button.disabled = true;
            button.textContent = "Eliminando...";

            await deleteProduct(button.dataset.deleteId);

            await loadInventory();

        } catch (error) {

            button.disabled = false;
            button.textContent = "Eliminar";

            showAlert(
                apiErrorEl,
                error.message || "No se pudo eliminar el producto.",
                "error"
            );
        }
    });
}


/* ---------- Ventas ---------- */

const salesLoadingEl =
    document.getElementById("sales-loading");

const salesTableEl =
    document.getElementById("sales-table");

const salesBodyEl =
    document.getElementById("sales-body");


const STATUS_LABELS = {
    completed: "Completado",
    refunded: "Reembolsado",
    pending: "Pendiente",
};


async function loadSales() {
    if (!salesBodyEl) return;

    try {

        if (salesLoadingEl) {
            salesLoadingEl.hidden = false;
        }

        if (salesTableEl) {
            salesTableEl.hidden = true;
        }

        const orders = await getOrders();

        if (!orders || orders.length === 0) {

            salesBodyEl.innerHTML = `
                <tr>
                    <td colspan="6">
                        No hay ventas registradas.
                    </td>
                </tr>
            `;

            if (salesLoadingEl) {
                salesLoadingEl.hidden = true;
            }

            if (salesTableEl) {
                salesTableEl.hidden = false;
            }

            return;
        }

        salesBodyEl.innerHTML = orders
            .map((order) => {

                const isRefunded =
                    order.status === "refunded";

                const orderDate = order.order_date
                    ? new Date(order.order_date).toLocaleDateString(
                        "es-CR"
                    )
                    : "—";

                const total = Number(
                    order.total_amount || 0
                );

                const status =
                    STATUS_LABELS[order.status] ||
                    order.status ||
                    "—";

                /*
                 * El backend ahora devuelve customer_name.
                 * Si por alguna razón no existe, usamos
                 * el ID como respaldo.
                 */
                const customerName =
                    order.customer_name ||
                    `Cliente #${order.customer_id}`;

                return `
                    <tr>

                        <td>
                            #${order.order_id}
                        </td>

                        <td>
                            ${customerName}
                        </td>

                        <td>
                            ${orderDate}
                        </td>

                        <td>
                            $${total.toFixed(2)}
                        </td>

                        <td>
                            ${status}
                        </td>

                        <td>
                            <button
                                type="button"
                                class="btn btn--outline"
                                data-refund-id="${order.order_id}"
                                ${isRefunded ? "disabled" : ""}
                            >
                                ${isRefunded
                        ? "Ya reembolsado"
                        : "Reembolsar"
                    }
                            </button>
                        </td>

                    </tr>
                `;
            })
            .join("");

        if (salesLoadingEl) {
            salesLoadingEl.hidden = true;
        }

        if (salesTableEl) {
            salesTableEl.hidden = false;
        }

    } catch (error) {

        if (salesLoadingEl) {
            salesLoadingEl.hidden = true;
        }

        showAlert(
            apiErrorEl,
            error.message || "No se pudieron cargar las ventas.",
            "error"
        );
    }
}


/* ---------- Reembolsar pedido ---------- */

if (salesBodyEl) {

    salesBodyEl.addEventListener("click", async (event) => {

        const button = event.target.closest("[data-refund-id]");

        if (!button || button.disabled) return;

        const confirmed = window.confirm(
            "¿Reembolsar este pedido? El stock de los productos se restaurará."
        );

        if (!confirmed) return;

        try {

            button.disabled = true;
            button.textContent = "Procesando...";

            await refundOrder(button.dataset.refundId);

            await loadSales();

            // El reembolso puede restaurar unidades al inventario.
            await loadInventory();

        } catch (error) {

            button.disabled = false;
            button.textContent = "Reembolsar";

            showAlert(
                apiErrorEl,
                error.message || "No se pudo procesar el reembolso.",
                "error"
            );
        }
    });
}


/* ---------- Inicialización ---------- */

if (hasAccess) {
    loadInventory();
    loadSales();
}
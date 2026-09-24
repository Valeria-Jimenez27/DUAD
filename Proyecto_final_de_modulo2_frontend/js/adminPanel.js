import { getProducts } from "./productService.js";
import { deleteProduct, getOrders, refundOrder } from "./adminService.js";
import { isLoggedIn, isAdmin } from "./storage.js";
import { showAlert, renderAccessRestricted } from "./ui.js";

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

const inventoryLoadingEl = document.getElementById("inventory-loading");
const inventoryTableEl = document.getElementById("inventory-table");
const inventoryBodyEl = document.getElementById("inventory-body");

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

        inventoryBodyEl.innerHTML = products
            .map(
                (product) => `
                    <tr>
                        <td>${product.name}</td>
                        <td>${product.brand || "—"}</td>
                        <td>${product.category || "—"}</td>
                        <td>$${Number(product.price || 0).toFixed(2)}</td>
                        <td>${Number(product.quantity || 0)}</td>
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
                `
            )
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
            await deleteProduct(button.dataset.deleteId);

            await loadInventory();
        } catch (error) {
            showAlert(
                apiErrorEl,
                error.message || "No se pudo eliminar el producto.",
                "error"
            );
        }
    });
}

/* ---------- Ventas ---------- */

const salesLoadingEl = document.getElementById("sales-loading");
const salesTableEl = document.getElementById("sales-table");
const salesBodyEl = document.getElementById("sales-body");

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

        salesBodyEl.innerHTML = orders
            .map((order) => {
                const isRefunded = order.status === "refunded";

                return `
                    <tr>
                        <td>#${order.order_id}</td>

                        <td>
                            Cliente #${order.customer_id}
                        </td>

                        <td>
                            ${new Date(order.order_date).toLocaleDateString(
                    "es-CR"
                )}
                        </td>

                        <td>
                            $${Number(order.total_amount || 0).toFixed(2)}
                        </td>

                        <td>
                            ${STATUS_LABELS[order.status] || order.status}
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
            await refundOrder(button.dataset.refundId);

            await loadSales();

            // Actualizamos también el inventario porque el reembolso
            // puede devolver unidades al stock.
            await loadInventory();
        } catch (error) {
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
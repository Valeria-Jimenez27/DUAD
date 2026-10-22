
import { getCart, removeItemFromCart } from "./orderService.js";
import { getCartId, isLoggedIn } from "./storage.js";
import { showAlert, renderAccessRestricted, escapeHtml } from "./ui.js";
import { getProductImage } from "./productImage.js";

const pageContentEl = document.getElementById("page-content");
const accessRestrictedEl = document.getElementById("access-restricted");
const loadingEl = document.getElementById("cart-loading");
const emptyEl = document.getElementById("empty-cart");
const contentEl = document.getElementById("cart-content");
const itemsEl = document.getElementById("cart-items");
const totalEl = document.getElementById("cart-total");
const apiErrorEl = document.getElementById("api-error");
const checkoutBtn = document.getElementById("checkout-btn");

if (!isLoggedIn()) {
    if (pageContentEl) pageContentEl.hidden = true;

    renderAccessRestricted(accessRestrictedEl, {
        title: "Debes iniciar sesión para continuar",
        message: "Inicia sesión para ver los productos que agregaste a tu carrito.",
        buttonText: "Ir a iniciar sesión",
        buttonHref: "login.html",
    });
}

function renderCart(cart) {
    const items = Array.isArray(cart?.items) ? cart.items : [];

    if (items.length === 0) {
        if (loadingEl) loadingEl.hidden = true;
        if (contentEl) contentEl.hidden = true;
        if (emptyEl) emptyEl.hidden = false;
        return;
    }

    if (!itemsEl || !totalEl) {
        throw new Error("No se encontraron los elementos necesarios para mostrar el carrito.");
    }

    itemsEl.innerHTML = items.map((item) => {
        const productName = escapeHtml(item.product_name ?? "Producto");
        const itemId = escapeHtml(item.cart_item_id ?? "");
        const productId = item.product_id;
        const unitPrice = Number(item.unit_price);
        const subtotal = Number(item.subtotal);
        const quantity = Number(item.quantity);

        return `
            <div class="cart-item-card" data-item-id="${itemId}">
                <img
                    src="${getProductImage({ product_id: productId })}"
                    alt="${productName}"
                    class="cart-item-card__image"
                />
                <div class="cart-item-card__info">
                    <h3>${productName}</h3>
                    <span class="text-muted">
                        Precio: $${Number.isFinite(unitPrice) ? unitPrice.toFixed(2) : "0.00"}
                        · Cantidad: ${Number.isFinite(quantity) ? quantity : 0}
                    </span>
                </div>
                <strong>
                    $${Number.isFinite(subtotal) ? subtotal.toFixed(2) : "0.00"}
                </strong>
                <button
                    type="button"
                    class="cart-item-card__remove"
                    data-item-id="${itemId}"
                >
                    🗑 Eliminar
                </button>
            </div>
        `;
    }).join("");

    totalEl.textContent = `$${Number(cart.total ?? 0).toFixed(2)}`;

    if (loadingEl) loadingEl.hidden = true;
    if (emptyEl) emptyEl.hidden = true;
    if (contentEl) contentEl.hidden = false;

    if (checkoutBtn) checkoutBtn.disabled = false;
}

async function loadCart() {
    if (loadingEl) loadingEl.hidden = false;
    if (emptyEl) emptyEl.hidden = true;
    if (contentEl) contentEl.hidden = true;

    if (apiErrorEl) {
        apiErrorEl.hidden = true;
        apiErrorEl.textContent = "";
    }

    const cartId = getCartId();

    if (!cartId) {
        if (loadingEl) loadingEl.hidden = true;
        if (contentEl) contentEl.hidden = true;
        if (emptyEl) emptyEl.hidden = false;
        return;
    }

    try {
        const cart = await getCart(cartId);
        renderCart(cart);
    } catch (error) {
        if (loadingEl) loadingEl.hidden = true;

        if (checkoutBtn) checkoutBtn.disabled = true;

        showAlert(
            apiErrorEl,
            error?.message || "No se pudo cargar el carrito.",
            "error"
        );
    }
}

if (itemsEl) {
    itemsEl.addEventListener("click", async (event) => {
        const button = event.target.closest(".cart-item-card__remove");

        if (!button) return;

        const cartId = getCartId();
        const itemId = button.dataset.itemId;

        if (!cartId || !itemId) {
            showAlert(apiErrorEl, "No se pudo identificar el artículo que deseas eliminar.", "error");
            return;
        }

        button.disabled = true;
        button.textContent = "Quitando...";

        try {
            await removeItemFromCart(cartId, itemId);
            await loadCart();
        } catch (error) {
            showAlert(
                apiErrorEl,
                error?.message || "No se pudo eliminar el artículo.",
                "error"
            );

            button.disabled = false;
            button.textContent = "🗑 Eliminar";
        }
    });
}

if (isLoggedIn()) {
    loadCart();
}

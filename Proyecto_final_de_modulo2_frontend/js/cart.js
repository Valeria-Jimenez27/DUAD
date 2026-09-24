/* ==========================================================================
   cart.js — Lógica de la página cart.html.
   ========================================================================== */

import { getCart, removeItemFromCart } from "./orderService.js";
import { getCartId, isLoggedIn } from "./storage.js";
import { showAlert, renderAccessRestricted } from "./ui.js";
import { getProductImage } from "./productImage.js";

const loadingEl = document.getElementById("cart-loading");
const emptyEl = document.getElementById("empty-cart");
const contentEl = document.getElementById("cart-content");
const itemsEl = document.getElementById("cart-items");
const totalEl = document.getElementById("cart-total");
const apiErrorEl = document.getElementById("api-error");
const checkoutBtn = document.getElementById("checkout-btn");


if (!isLoggedIn()) {
    document.getElementById("page-content").hidden = true;
    renderAccessRestricted(document.getElementById("access-restricted"), {
        title: "Debes iniciar sesión para continuar",
        message: "Inicia sesión para ver los productos que agregaste a tu carrito.",
        buttonText: "Ir a iniciar sesión",
        buttonHref: "login.html",
    });
}

function renderCart(cart) {
    if (!cart.items || cart.items.length === 0) {
        loadingEl.hidden = true;
        emptyEl.hidden = false;
        return;
    }

    itemsEl.innerHTML = cart.items
        .map(
            (item) => `
        <div class="cart-item-card" data-item-id="${item.cart_item_id}">
          <img src="${getProductImage({ product_id: item.product_id })}" alt="${item.product_name}" class="cart-item-card__image" />
          <div class="cart-item-card__info">
            <h3>${item.product_name}</h3>
            <span class="text-muted">Precio: $${Number(item.unit_price).toFixed(2)} · Cantidad: ${item.quantity}</span>
          </div>
          <strong>$${Number(item.subtotal).toFixed(2)}</strong>
          <button type="button" class="cart-item-card__remove" data-item-id="${item.cart_item_id}">🗑 Eliminar</button>
        </div>
      `
        )
        .join("");

    totalEl.textContent = `$${Number(cart.total || 0).toFixed(2)}`;

    loadingEl.hidden = true;
    contentEl.hidden = false;
}

async function loadCart() {
    const cartId = getCartId();

    if (!cartId) {
        loadingEl.hidden = true;
        emptyEl.hidden = false;
        return;
    }

    try {
        const cart = await getCart(cartId);
        renderCart(cart);
    } catch (error) {
        loadingEl.hidden = true;
        showAlert(apiErrorEl, error.message, "error");
    }
}

itemsEl.addEventListener("click", async (event) => {
    const button = event.target.closest(".cart-item-card__remove");
    if (!button) return;

    const cartId = getCartId();
    const itemId = button.dataset.itemId;
    button.disabled = true;
    button.textContent = "Quitando...";

    try {
        await removeItemFromCart(cartId, itemId);
        loadCart(); // recarga para reflejar el total actualizado
    } catch (error) {
        showAlert(apiErrorEl, error.message, "error");
        button.disabled = false;
        button.textContent = "🗑 Eliminar";
    }
});

if (isLoggedIn()) {
    loadCart();
}
import { getCart, checkout } from "./orderService.js";
import { getCartId, isLoggedIn, clearCartId } from "./storage.js";
import { validateField } from "./validators.js";
import { showAlert, clearAlert, setFieldError, setLoading, renderAccessRestricted } from "./ui.js";

const loadingEl = document.getElementById("summary-loading");
const contentEl = document.getElementById("summary-content");
const itemsEl = document.getElementById("summary-items");
const totalEl = document.getElementById("summary-total");
const apiErrorEl = document.getElementById("api-error");

const form = document.getElementById("checkout-form");
const addressInput = document.getElementById("billing-address");
const paymentSelect = document.getElementById("payment-method");
const addressError = document.getElementById("billing-address-error");
const paymentError = document.getElementById("payment-method-error");
const formAlert = document.getElementById("form-alert");
const submitBtn = document.getElementById("submit-btn");

const pageContentEl = document.getElementById("page-content");
const accessRestrictedEl = document.getElementById("access-restricted");

if (!isLoggedIn()) {
    pageContentEl.hidden = true;
    renderAccessRestricted(accessRestrictedEl, {
        title: "Debes iniciar sesión para continuar",
        message: "Inicia sesión para revisar y confirmar tu pedido.",
        buttonText: "Ir a iniciar sesión",
        buttonHref: "login.html",
    });
}

const cartId = getCartId();

if (isLoggedIn() && !cartId) {
    window.location.href = "cart.html";
}

function renderSummary(cart) {
    if (!cart.items || cart.items.length === 0) {
        window.location.href = "cart.html";
        return;
    }

    itemsEl.innerHTML = cart.items
        .map(
            (item) => `
        <div class="cart-item">
          <div class="cart-item__info">
            <h3>${item.product_name}</h3>
            <span class="text-muted">${item.quantity} × $${Number(item.unit_price).toFixed(2)}</span>
          </div>
          <span class="product-card__price">$${Number(item.subtotal).toFixed(2)}</span>
        </div>
      `
        )
        .join("");

    totalEl.textContent = `$${Number(cart.total || 0).toFixed(2)}`;

    loadingEl.hidden = true;
    contentEl.hidden = false;
}

async function loadSummary() {
    try {
        const cart = await getCart(cartId);
        renderSummary(cart);
    } catch (error) {
        loadingEl.hidden = true;
        showAlert(apiErrorEl, error.message, "error");
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearAlert(formAlert);

    const addressMsg = validateField(addressInput.value, "required");
    const paymentMsg = validateField(paymentSelect.value, "required");

    setFieldError(addressInput, addressError, addressMsg);
    setFieldError(paymentSelect, paymentError, paymentMsg);

    if (addressMsg || paymentMsg) return;

    const restoreButton = setLoading(submitBtn, "Procesando...");

    try {
        const result = await checkout(cartId, {
            billingAddress: addressInput.value.trim(),
            paymentMethod: paymentSelect.value,
        });

        clearCartId();

        window.location.href = `purchase-complete.html?order_id=${result.order_id}`;
    } catch (error) {
        showAlert(formAlert, error.message, "error");
    } finally {
        restoreButton();
    }
});

if (isLoggedIn() && cartId) {
    loadSummary();
}
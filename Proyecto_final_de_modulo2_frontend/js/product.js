import { getProductById } from "./productService.js";
import { addItemToCart } from "./orderService.js";
import { isLoggedIn, getCustomerId } from "./storage.js";
import { showAlert, setLoading, renderAccessRestricted } from "./ui.js";
import { getProductImage } from "./productImage.js";

const loadingEl = document.getElementById("product-loading");
const detailEl = document.getElementById("product-detail");
const apiErrorEl = document.getElementById("api-error");
const addToCartAlertEl = document.getElementById("add-to-cart-alert");

const imageEl = document.getElementById("product-image");
const nameEl = document.getElementById("product-name");
const metaEl = document.getElementById("product-meta");
const priceEl = document.getElementById("product-price");
const stockBadgeEl = document.getElementById("product-stock-badge");
const quantityInput = document.getElementById("quantity");
const addToCartBtn = document.getElementById("add-to-cart-btn");

if (!isLoggedIn()) {
    document.getElementById("page-content").hidden = true;
    renderAccessRestricted(document.getElementById("access-restricted"), {
        title: "Debes iniciar sesión para continuar",
        message: "Inicia sesión para ver el detalle de este producto y comprarlo.",
        buttonText: "Ir a iniciar sesión",
        buttonHref: "login.html",
    });
}

const params = new URLSearchParams(window.location.search);
const productId = params.get("id");

let currentProduct = null;

function renderProduct(product) {
    currentProduct = product;
    const inStock = product.quantity > 0;
    imageEl.src = getProductImage(product);
    imageEl.alt = product.name;
    nameEl.textContent = product.name;
    metaEl.textContent = `${product.brand || "Sin marca"} · ${product.category || "General"}`;
    priceEl.textContent = `$${Number(product.price).toFixed(2)}`;

    stockBadgeEl.textContent = inStock ? `${product.quantity} en stock` : "Agotado";
    stockBadgeEl.className = `badge ${inStock ? "badge--stock" : "badge--out"}`;

    quantityInput.max = product.quantity;
    addToCartBtn.disabled = !inStock;
    if (!inStock) addToCartBtn.textContent = "Sin stock disponible";

    loadingEl.hidden = true;
    detailEl.hidden = false;
}

async function loadProduct() {
    if (!productId) {
        showAlert(apiErrorEl, "No se especificó ningún producto.", "error");
        loadingEl.hidden = true;
        return;
    }

    try {
        const product = await getProductById(productId);
        renderProduct(product);
    } catch (error) {
        loadingEl.hidden = true;
        showAlert(apiErrorEl, error.message, "error");
    }
}

addToCartBtn.addEventListener("click", async () => {
    if (!getCustomerId()) {
        showAlert(
            addToCartAlertEl,
            "Tu cuenta no tiene un perfil de cliente asociado. Contacta al administrador.",
            "error"
        );
        return;
    }

    const quantity = Number(quantityInput.value);

    if (!quantity || quantity < 1) {
        showAlert(addToCartAlertEl, "Ingresa una cantidad válida.", "error");
        return;
    }

    if (quantity > currentProduct.quantity) {
        showAlert(addToCartAlertEl, `Solo hay ${currentProduct.quantity} unidades disponibles.`, "error");
        return;
    }

    const restoreButton = setLoading(addToCartBtn, "Agregando...");

    try {
        await addItemToCart(Number(productId), quantity);
        window.location.href = "cart.html";
    } catch (error) {
        showAlert(addToCartAlertEl, error.message, "error");
    } finally {
        restoreButton();
    }
});

if (isLoggedIn()) {
    loadProduct();
}

import { getProductById } from "./productService.js";
import { addItemToCart } from "./orderService.js";
import { isLoggedIn, getCustomerId } from "./storage.js";
import {
    showAlert,
    setLoading,
    renderAccessRestricted
} from "./ui.js";
import { getProductImage } from "./productImage.js";

const loadingEl = document.getElementById("product-loading");
const detailEl = document.getElementById("product-detail");
const apiErrorEl = document.getElementById("api-error");
const addToCartAlertEl = document.getElementById("add-to-cart-alert");
const pageContentEl = document.getElementById("page-content");
const accessRestrictedEl = document.getElementById("access-restricted");

const imageEl = document.getElementById("product-image");
const nameEl = document.getElementById("product-name");
const metaEl = document.getElementById("product-meta");
const priceEl = document.getElementById("product-price");
const stockBadgeEl = document.getElementById("product-stock-badge");
const quantityInput = document.getElementById("quantity");
const addToCartBtn = document.getElementById("add-to-cart-btn");

const loggedIn = isLoggedIn();

if (!loggedIn) {
    if (pageContentEl) {
        pageContentEl.hidden = true;
    }

    renderAccessRestricted(accessRestrictedEl, {
        title: "Debes iniciar sesión para continuar",
        message: "Inicia sesión para ver el detalle de este producto y comprarlo.",
        buttonText: "Ir a iniciar sesión",
        buttonHref: "login.html"
    });
}

const params = new URLSearchParams(window.location.search);
const productId = params.get("id");

let currentProduct = null;

function renderProduct(product) {
    if (!product || typeof product !== "object") {
        throw new Error("No se encontraron los datos del producto.");
    }

    const productName = product.name ?? "Producto sin nombre";
    const quantity = Number(product.quantity);
    const price = Number(product.price);

    if (!Number.isFinite(quantity) || !Number.isFinite(price)) {
        throw new Error("Los datos de precio o inventario del producto no son válidos.");
    }

    currentProduct = {
        ...product,
        name: productName,
        quantity,
        price
    };

    const inStock = quantity > 0;

    imageEl.src = getProductImage(currentProduct);
    imageEl.alt = productName;

    nameEl.textContent = productName;
    metaEl.textContent =
        `${product.brand || "Sin marca"} · ${product.category || "General"}`;

    priceEl.textContent = `$${price.toFixed(2)}`;

    stockBadgeEl.textContent = inStock
        ? `${quantity} en stock`
        : "Agotado";

    stockBadgeEl.className = `badge ${
        inStock ? "badge--stock" : "badge--out"
    }`;

    quantityInput.min = "1";
    quantityInput.max = String(Math.max(0, quantity));
    quantityInput.value = "1";
    quantityInput.disabled = !inStock;

    addToCartBtn.disabled = !inStock;
    addToCartBtn.textContent = inStock
        ? "Agregar al carrito"
        : "Sin stock disponible";

    loadingEl.hidden = true;
    detailEl.hidden = false;
}

async function loadProduct() {
    if (!productId || !Number.isInteger(Number(productId)) || Number(productId) <= 0) {
        loadingEl.hidden = true;
        showAlert(apiErrorEl, "El identificador del producto no es válido.", "error");
        return;
    }

    try {
        const product = await getProductById(productId);
        renderProduct(product);
    } catch (error) {
        loadingEl.hidden = true;
        showAlert(
            apiErrorEl,
            error?.message || "No se pudo cargar el producto.",
            "error"
        );
    }
}

if (addToCartBtn) {
    addToCartBtn.addEventListener("click", async () => {
        if (!currentProduct) {
            showAlert(
                addToCartAlertEl,
                "Espera a que cargue la información del producto.",
                "error"
            );
            return;
        }

        if (!getCustomerId()) {
            showAlert(
                addToCartAlertEl,
                "Tu cuenta no tiene un perfil de cliente asociado. Contacta al administrador.",
                "error"
            );
            return;
        }

        const quantity = Number(quantityInput.value);

        if (!Number.isInteger(quantity) || quantity < 1) {
            showAlert(
                addToCartAlertEl,
                "Ingresa una cantidad entera mayor que cero.",
                "error"
            );
            return;
        }

        if (quantity > currentProduct.quantity) {
            showAlert(
                addToCartAlertEl,
                `Solo hay ${currentProduct.quantity} unidades disponibles.`,
                "error"
            );
            return;
        }

        const restoreButton = setLoading(addToCartBtn, "Agregando...");

        try {
            await addItemToCart(Number(productId), quantity);
            window.location.href = "cart.html";
        } catch (error) {
            showAlert(
                addToCartAlertEl,
                error?.message || "No se pudo agregar el producto al carrito.",
                "error"
            );
        } finally {
            restoreButton();
        }
    });
}

if (loggedIn) {
    loadProduct();
}

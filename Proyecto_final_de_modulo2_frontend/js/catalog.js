import { getProducts } from "./productService.js";
import { addItemToCart } from "./orderService.js";
import {
    isLoggedIn,
    getCustomerId
} from "./storage.js";
import {
    showAlert,
    setLoading,
    renderAccessRestricted
} from "./ui.js";
import { getProductImage } from "./productImage.js";


const loadingEl =
    document.getElementById("catalog-loading");

const gridEl =
    document.getElementById("product-grid");

const emptyStateEl =
    document.getElementById("empty-state");

const noResultsStateEl =
    document.getElementById("no-results-state");

const apiErrorEl =
    document.getElementById("api-error");

const quickAddAlertEl =
    document.getElementById("quick-add-alert");

const pageContentEl =
    document.getElementById("page-content");

const accessRestrictedEl =
    document.getElementById("access-restricted");

const toolbarEl =
    document.getElementById("catalog-toolbar");

const searchInput =
    document.getElementById("search-input");

const availableOnlyCheckbox =
    document.getElementById(
        "available-only-checkbox"
    );


let allProducts = [];


/* =========================================================
   PARÁMETROS DE LA URL
   ========================================================= */

const urlParams =
    new URLSearchParams(
        window.location.search
    );

const initialSearch =
    urlParams.get("search") || "";

const selectedCategory =
    urlParams.get("category") || "";


/*
 * Si venimos desde la búsqueda del encabezado,
 * mostramos el texto en el buscador.
 */
if (searchInput && initialSearch) {
    searchInput.value = initialSearch;
}


/* =========================================================
   ACCESO
   ========================================================= */

if (!isLoggedIn()) {

    pageContentEl.hidden = true;

    renderAccessRestricted(
        accessRestrictedEl,
        {
            title:
                "Debes iniciar sesión para continuar",

            message:
                "Inicia sesión para ver el catálogo y comprar productos para tu mascota.",

            buttonText:
                "Ir a iniciar sesión",

            buttonHref:
                "login.html"
        }
    );
}


/* =========================================================
   NORMALIZAR TEXTO
   ========================================================= */

function normalizeText(value) {

    return String(value || "")
        .trim()
        .toLowerCase()
        .normalize("NFD")
        .replace(
            /[\u0300-\u036f]/g,
            ""
        );
}


/* =========================================================
   PRODUCTOS
   ========================================================= */

function renderProducts(products) {

    gridEl.innerHTML =
        products
            .map((product) => {

                const inStock =
                    Number(product.quantity) > 0;

                return `
                    <div class="product-card">

                        <a
                            href="product.html?id=${product.product_id}"
                            class="product-card__link"
                        >

                            <img
                                src="${getProductImage(product)}"
                                alt="${product.name}"
                                class="product-card__image"
                            />

                            <div class="product-card__body">

                                <span
                                    class="badge ${inStock
                        ? "badge--stock"
                        : "badge--out"
                    }"
                                >
                                    ${inStock
                        ? `${product.quantity} en stock`
                        : "Agotado"
                    }
                                </span>

                                <h3>
                                    ${product.name}
                                </h3>

                                <span class="text-muted">
                                    ${product.brand || "Sin marca"}
                                    ·
                                    ${product.category || "General"}
                                </span>

                                <span class="product-card__price">
                                    $${Number(product.price).toFixed(2)}
                                </span>

                            </div>

                        </a>

                        <button
                            type="button"
                            class="btn btn--primary btn--full product-card__quick-add"
                            data-product-id="${product.product_id}"
                            ${inStock ? "" : "disabled"}
                        >
                            ${inStock
                        ? "Agregar al carrito"
                        : "Sin stock"
                    }
                        </button>

                    </div>
                `;
            })
            .join("");

    gridEl.hidden = false;
}


/* =========================================================
   FILTROS
   ========================================================= */

function applyFilters() {

    const query =
        normalizeText(
            searchInput.value
        );

    const category =
        normalizeText(
            selectedCategory
        );

    const onlyAvailable =
        availableOnlyCheckbox.checked;


    const filtered =
        allProducts.filter(
            (product) => {

                const productName =
                    normalizeText(
                        product.name
                    );

                const productBrand =
                    normalizeText(
                        product.brand
                    );

                const productCategory =
                    normalizeText(
                        product.category
                    );


                const matchesQuery =
                    !query ||
                    productName.includes(query) ||
                    productBrand.includes(query) ||
                    productCategory.includes(query);


                const matchesCategory =
                    !category ||
                    productCategory === category;


                const matchesAvailability =
                    !onlyAvailable ||
                    Number(product.quantity) > 0;


                return (
                    matchesQuery &&
                    matchesCategory &&
                    matchesAvailability
                );
            }
        );


    if (filtered.length === 0) {

        gridEl.hidden = true;

        noResultsStateEl.hidden = false;

    } else {

        noResultsStateEl.hidden = true;

        renderProducts(filtered);
    }
}


/* =========================================================
   EVENTOS DE FILTROS
   ========================================================= */

searchInput.addEventListener(
    "input",
    applyFilters
);

availableOnlyCheckbox.addEventListener(
    "change",
    applyFilters
);


/* =========================================================
   CARGAR CATÁLOGO
   ========================================================= */

async function loadCatalog() {

    try {

        const products =
            await getProducts();

        loadingEl.hidden = true;


        if (
            !products ||
            products.length === 0
        ) {

            emptyStateEl.hidden = false;

            return;
        }


        allProducts = products;

        toolbarEl.hidden = false;

        applyFilters();

    } catch (error) {

        loadingEl.hidden = true;

        showAlert(
            apiErrorEl,
            error.message,
            "error"
        );
    }
}


/* =========================================================
   AGREGAR AL CARRITO
   ========================================================= */

gridEl.addEventListener(
    "click",
    async (event) => {

        const button =
            event.target.closest(
                ".product-card__quick-add"
            );

        if (
            !button ||
            button.disabled
        ) {
            return;
        }


        if (!getCustomerId()) {

            showAlert(
                quickAddAlertEl,
                "Tu cuenta no tiene un perfil de cliente asociado. Contacta al administrador.",
                "error"
            );

            return;
        }


        const productId =
            Number(
                button.dataset.productId
            );

        const restoreButton =
            setLoading(
                button,
                "Agregando..."
            );


        try {

            await addItemToCart(
                productId,
                1
            );

            button.textContent =
                "✓ Agregado";


            setTimeout(
                () => {
                    restoreButton();
                },
                1200
            );

        } catch (error) {

            restoreButton();

            showAlert(
                quickAddAlertEl,
                error.message,
                "error"
            );
        }
    }
);


/* =========================================================
   INICIO
   ========================================================= */

if (isLoggedIn()) {
    loadCatalog();
}
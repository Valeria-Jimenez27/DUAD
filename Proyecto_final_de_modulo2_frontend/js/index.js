import { getProducts } from "./productService.js";
import { escapeHtml } from "./ui.js";


const categoryGrid =
    document.getElementById("category-grid");

const categoryLoading =
    document.getElementById("category-loading");


const CATEGORY_ICONS = {
    alimento: "🍖",
    alimentos: "🍖",
    farmacia: "💊",
    snacks: "🦴",
    accesorios: "🐾",
    higiene: "🧼",
    juguetes: "🧸",
    default: "🐾"
};


document.addEventListener(
    "DOMContentLoaded",
    init
);


async function init() {

    if (!categoryGrid) {
        return;
    }

    try {

        const products =
            await getProducts();

        renderCategories(products);

    } catch (error) {

        console.error(
            "Error cargando categorías:",
            error
        );

        if (categoryLoading) {
            categoryLoading.textContent =
                "No fue posible cargar las categorías.";
        }
    }
}


function renderCategories(products) {

    const categories =
        getCategories(products);

    categoryGrid.innerHTML = "";

    if (categories.length === 0) {

        categoryGrid.innerHTML = `
            <p class="text-muted">
                No hay categorías disponibles.
            </p>
        `;

        return;
    }


    categories.forEach(
        (category) => {

            const card =
                document.createElement("a");

            card.className =
                "category-card";

            card.href =
                `catalog.html?category=${encodeURIComponent(
                    category
                )}`;

            const icon =
                getCategoryIcon(category);

            card.innerHTML = `
                <span
                    class="category-card__icon"
                    aria-hidden="true"
                >
                    ${icon}
                </span>

                <strong>
                    ${escapeHtml(
                formatCategoryName(category)
            )}
                </strong>
            `;

            categoryGrid.appendChild(card);
        }
    );
}


function getCategories(products) {

    const categories =
        new Set();


    products.forEach(
        (product) => {

            /*
             * La API utiliza "category".
             * Se elimina el fallback "categoria"
             * porque los identificadores del proyecto
             * deben mantenerse en inglés.
             */
            const category =
                product.category ??
                product.categoryName;

            if (category) {
                categories.add(
                    String(category).trim()
                );
            }
        }
    );


    return Array.from(categories).sort(
        (a, b) =>
            a.localeCompare(b, "es")
    );
}


function getCategoryIcon(category) {

    const normalized =
        String(category)
            .toLowerCase()
            .normalize("NFD")
            .replace(
                /[\u0300-\u036f]/g,
                ""
            );

    return (
        CATEGORY_ICONS[normalized] ??
        CATEGORY_ICONS.default
    );
}


function formatCategoryName(category) {

    const text =
        String(category).trim();

    if (!text) {
        return "";
    }

    return (
        text.charAt(0).toUpperCase() +
        text.slice(1)
    );
}
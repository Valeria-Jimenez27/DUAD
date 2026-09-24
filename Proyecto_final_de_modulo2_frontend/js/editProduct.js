import {
    getProductById,
    getBrands,
    getCategories
} from "./productService.js";

import {
    createProduct,
    updateProduct
} from "./adminService.js";

import {
    isLoggedIn,
    isAdmin
} from "./storage.js";

import {
    validateField
} from "./validators.js";

import {
    showAlert,
    clearAlert,
    setFieldError,
    setLoading,
    renderAccessRestricted
} from "./ui.js";


const pageContentEl =
    document.getElementById("page-content");

const accessRestrictedEl =
    document.getElementById("access-restricted");


let hasAccess = true;


/* =========================================================
   CONTROL DE ACCESO
   ========================================================= */

if (!isLoggedIn()) {

    hasAccess = false;

    pageContentEl.hidden = true;

    renderAccessRestricted(
        accessRestrictedEl,
        {
            title:
                "Debes iniciar sesión para continuar",

            message:
                "Inicia sesión con una cuenta de administrador para gestionar productos.",

            buttonText:
                "Ir a iniciar sesión",

            buttonHref:
                "login.html"
        }
    );

} else if (!isAdmin()) {

    hasAccess = false;

    pageContentEl.hidden = true;

    renderAccessRestricted(
        accessRestrictedEl,
        {
            title:
                "No tienes permisos de administrador",

            message:
                "Editar o crear productos es exclusivo para cuentas de administrador.",

            buttonText:
                "Volver al catálogo",

            buttonHref:
                "catalog.html"
        }
    );
}


/* =========================================================
   ELEMENTOS
   ========================================================= */

const params =
    new URLSearchParams(
        window.location.search
    );

const productId =
    params.get("id");


const form =
    document.getElementById("product-form");

const formTitle =
    document.getElementById("form-title");

const submitBtn =
    document.getElementById("submit-btn");

const formAlert =
    document.getElementById("form-alert");


const nameInput =
    document.getElementById("name");

const priceInput =
    document.getElementById("price");

const quantityInput =
    document.getElementById("quantity");

const brandSelect =
    document.getElementById("brand");

const categorySelect =
    document.getElementById("category");

const imageInput =
    document.getElementById("image");

const imagePreviewContainer =
    document.getElementById(
        "image-preview-container"
    );

const imagePreview =
    document.getElementById(
        "image-preview"
    );


const nameError =
    document.getElementById(
        "name-error"
    );

const priceError =
    document.getElementById(
        "price-error"
    );

const quantityError =
    document.getElementById(
        "quantity-error"
    );

const brandError =
    document.getElementById(
        "brand-error"
    );

const categoryError =
    document.getElementById(
        "category-error"
    );

const imageError =
    document.getElementById(
        "image-error"
    );


/*
 * Imagen actual del producto.
 *
 * Si estamos editando y no seleccionamos una nueva,
 * conservaremos esta imagen.
 */

let currentImage = "";


/* =========================================================
   TÍTULO
   ========================================================= */

if (productId) {

    formTitle.textContent =
        "Editar producto";

    submitBtn.textContent =
        "Guardar cambios";
}


/* =========================================================
   SELECTS
   ========================================================= */

function populateSelect(
    selectEl,
    items,
    idKey,
    nameKey
) {

    items.forEach(
        (item) => {

            const option =
                document.createElement(
                    "option"
                );

            option.value =
                item[idKey];

            option.textContent =
                item[nameKey];

            selectEl.appendChild(
                option
            );
        }
    );
}


/* =========================================================
   VISTA PREVIA DE IMAGEN
   ========================================================= */

function showImagePreview(
    imageSource
) {

    if (!imageSource) {

        imagePreviewContainer.hidden =
            true;

        imagePreview.removeAttribute(
            "src"
        );

        return;
    }


    imagePreview.src =
        imageSource;

    imagePreviewContainer.hidden =
        false;
}


/* =========================================================
   LEER IMAGEN
   ========================================================= */

function readImageFile(file) {

    return new Promise(
        (resolve, reject) => {

            const reader =
                new FileReader();


            reader.addEventListener(
                "load",
                () => {

                    resolve(
                        reader.result
                    );
                }
            );


            reader.addEventListener(
                "error",
                () => {

                    reject(
                        new Error(
                            "No se pudo leer la imagen."
                        )
                    );
                }
            );


            reader.readAsDataURL(
                file
            );
        }
    );
}


/* =========================================================
   CAMBIO DE FOTO
   ========================================================= */

imageInput.addEventListener(
    "change",
    async () => {

        const file =
            imageInput.files?.[0];


        imageError.textContent =
            "";

        imageInput.classList.remove(
            "is-invalid"
        );


        if (!file) {

            showImagePreview(
                currentImage
            );

            return;
        }


        const validTypes = [
            "image/jpeg",
            "image/png",
            "image/webp"
        ];


        if (
            !validTypes.includes(
                file.type
            )
        ) {

            const message =
                "La imagen debe ser JPG, PNG o WebP.";

            setFieldError(
                imageInput,
                imageError,
                message
            );

            imageInput.value = "";

            return;
        }


        /*
         * Máximo 1.5 MB.
         *
         * Esto evita llenar rápidamente
         * el localStorage con imágenes enormes.
         */

        const maxSize =
            1.5 * 1024 * 1024;


        if (
            file.size > maxSize
        ) {

            const message =
                "La imagen no puede superar 1.5 MB.";

            setFieldError(
                imageInput,
                imageError,
                message
            );

            imageInput.value = "";

            return;
        }


        try {

            const imageData =
                await readImageFile(
                    file
                );

            currentImage =
                imageData;

            showImagePreview(
                currentImage
            );

        } catch (error) {

            setFieldError(
                imageInput,
                imageError,
                error.message
            );
        }
    }
);


/* =========================================================
   CARGAR MARCAS, CATEGORÍAS Y PRODUCTO
   ========================================================= */

async function loadFormData() {

    try {

        const [
            brands,
            categories
        ] = await Promise.all(
            [
                getBrands(),
                getCategories()
            ]
        );


        populateSelect(
            brandSelect,
            brands,
            "brand_id",
            "brand_name"
        );


        populateSelect(
            categorySelect,
            categories,
            "category_id",
            "category_name"
        );


        /*
         * Si estamos editando,
         * cargar datos existentes.
         */

        if (productId) {

            const product =
                await getProductById(
                    productId
                );


            nameInput.value =
                product.name;

            priceInput.value =
                product.price;

            quantityInput.value =
                product.quantity;


            const matchingBrand =
                brands.find(
                    (brand) =>
                        brand.brand_name ===
                        product.brand
                );


            const matchingCategory =
                categories.find(
                    (category) =>
                        category.category_name ===
                        product.category
                );


            if (matchingBrand) {

                brandSelect.value =
                    matchingBrand.brand_id;
            }


            if (matchingCategory) {

                categorySelect.value =
                    matchingCategory.category_id;
            }


            /*
             * Mostrar imagen existente.
             */

            if (
                typeof product.image ===
                "string" &&
                product.image.trim() !== ""
            ) {

                currentImage =
                    product.image;

                showImagePreview(
                    currentImage
                );
            }
        }

    } catch (error) {

        showAlert(
            formAlert,
            error.message,
            "error"
        );
    }
}


/* =========================================================
   VALIDACIÓN
   ========================================================= */

function validateForm() {

    let isValid = true;


    const nameMsg =
        validateField(
            nameInput.value,
            "required"
        );

    setFieldError(
        nameInput,
        nameError,
        nameMsg
    );


    if (nameMsg) {
        isValid = false;
    }


    const priceMsg =
        !priceInput.value ||
            Number(priceInput.value) <= 0
            ? "Ingresa un precio mayor a 0."
            : null;


    setFieldError(
        priceInput,
        priceError,
        priceMsg
    );


    if (priceMsg) {
        isValid = false;
    }


    const quantityValue =
        Number(quantityInput.value);


    const quantityMsg =
        quantityInput.value === "" ||
            !Number.isInteger(
                quantityValue
            ) ||
            quantityValue < 0
            ? "Ingresa una cantidad válida (0 o más)."
            : null;


    setFieldError(
        quantityInput,
        quantityError,
        quantityMsg
    );


    if (quantityMsg) {
        isValid = false;
    }


    const brandMsg =
        validateField(
            brandSelect.value,
            "required"
        );


    setFieldError(
        brandSelect,
        brandError,
        brandMsg
    );


    if (brandMsg) {
        isValid = false;
    }


    const categoryMsg =
        validateField(
            categorySelect.value,
            "required"
        );


    setFieldError(
        categorySelect,
        categoryError,
        categoryMsg
    );


    if (categoryMsg) {
        isValid = false;
    }


    return isValid;
}


/* =========================================================
   GUARDAR
   ========================================================= */

form.addEventListener(
    "submit",
    async (event) => {

        event.preventDefault();

        clearAlert(formAlert);


        if (!validateForm()) {
            return;
        }


        /*
         * Si no seleccionamos una nueva imagen
         * y estamos editando, se conserva currentImage.
         *
         * Si es un producto nuevo y no seleccionamos
         * imagen, mockData colocará la imagen por defecto.
         */

        const payload = {

            name:
                nameInput.value.trim(),

            price:
                Number(
                    priceInput.value
                ),

            quantity:
                Number(
                    quantityInput.value
                ),

            brandId:
                Number(
                    brandSelect.value
                ),

            categoryId:
                Number(
                    categorySelect.value
                ),

            image:
                currentImage || ""
        };


        const restoreButton =
            setLoading(
                submitBtn,
                productId
                    ? "Guardando..."
                    : "Creando..."
            );


        try {

            if (productId) {

                await updateProduct(
                    productId,
                    payload
                );

            } else {

                await createProduct(
                    payload
                );
            }


            window.location.href =
                "admin-panel.html";

        } catch (error) {

            showAlert(
                formAlert,
                error.message,
                "error"
            );

        } finally {

            restoreButton();
        }
    }
);


/* =========================================================
   INICIO
   ========================================================= */

if (hasAccess) {
    loadFormData();
}
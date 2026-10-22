const DEFAULT_PRODUCT_IMAGE =
    "img/products/img-3.jpg";


const PRODUCT_IMAGES = {
    1: "img/products/food-1.jpg",
    2: "img/products/food-2.jpg",
    3: "img/products/food-3.jpg",
    4: "img/products/img-3.jpg",
    5: "img/products/food-4.jpg",
    6: "img/products/img-5.jpg",
    7: "img/products/img-4.jpg",
    8: "img/products/img-6.jpg"
};


export function getProductImage(product) {
    if (!product) {
        return DEFAULT_PRODUCT_IMAGE;
    }

    /*
     * Si el producto trae una imagen desde la API,
     * utilizamos esa imagen.
     */
    if (
        typeof product.image === "string" &&
        product.image.trim() !== ""
    ) {
        return normalizeImagePath(product.image);
    }


    /*
     * Compatibilidad con productos que utilicen
     * imageUrl en lugar de image.
     */
    if (
        typeof product.imageUrl === "string" &&
        product.imageUrl.trim() !== ""
    ) {
        return normalizeImagePath(product.imageUrl);
    }


    /*
     * Si no tiene imagen propia, utilizamos
     * la imagen asociada al ID del producto.
     */
    return (
        PRODUCT_IMAGES[
        Number(
            product.product_id ??
            product.id
        )
        ] || DEFAULT_PRODUCT_IMAGE
    );
}


function normalizeImagePath(path) {
    const cleanPath =
        String(path || "").replace(
            /^\.\//,
            ""
        );


    /*
     * Compatibilidad con rutas antiguas
     * utilizadas en el proyecto.
     */
    if (
        cleanPath ===
        "img/logo-header.jpg"
    ) {
        return "img/products/logo-header.jpg";
    }


    if (
        cleanPath ===
        "img/hero-bg.jpg"
    ) {
        return "img/products/hero-bg.jpg";
    }


    /*
     * Si la ruta comienza con img/
     * pero todavía no incluye products/,
     * la normalizamos.
     */
    if (
        cleanPath.startsWith("img/") &&
        !cleanPath.startsWith(
            "img/products/"
        )
    ) {
        return `img/products/${cleanPath.substring(4)}`;
    }


    return (
        cleanPath ||
        DEFAULT_PRODUCT_IMAGE
    );
}
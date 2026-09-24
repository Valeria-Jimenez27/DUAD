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
    if (!product) return "img/products/img-1.jpg";

    if (typeof product.image === "string" && product.image.trim() !== "") {
        return normalizeImagePath(product.image);
    }

    if (typeof product.imageUrl === "string" && product.imageUrl.trim() !== "") {
        return normalizeImagePath(product.imageUrl);
    }

    return PRODUCT_IMAGES[Number(product.product_id ?? product.id)] || "img/products/img-1.jpg";
}

function normalizeImagePath(path) {
    const cleanPath = String(path || "").replace(/^\.\//, "");

    if (cleanPath === "img/logo-header.jpg") return "img/products/logo-header.jpg";
    if (cleanPath === "img/hero-bg.jpg") return "img/products/hero-bg.jpg";

    if (cleanPath.startsWith("img/") && !cleanPath.startsWith("img/products/")) {
        return `img/products/${cleanPath.substring(4)}`;
    }

    return cleanPath || "img/products/img-1.jpg";
}

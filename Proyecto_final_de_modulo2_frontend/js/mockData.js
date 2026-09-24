import {
    getLocalCartItems,
    saveLocalCartItems,
    clearLocalCartItems
} from "./storage.js";


/* ==========================================================================
   MOCK DATA
   Permite mostrar toda la app sin backend/Redis corriendo.
   ========================================================================== */


/* ==========================================================================
   UTILIDADES
   ========================================================================== */

function delay(ms = 350) {
    return new Promise((resolve) => setTimeout(resolve, ms));
}


/* ==========================================================================
   CONFIGURACIÓN
   ========================================================================== */

export const MOCK_ADMIN_EMAIL =
    "admin@valespetstore.com";


/* ==========================================================================
   MARCAS
   ========================================================================== */

export const MOCK_BRANDS = [
    {
        brand_id: 1,
        brand_name: "NutriSource"
    },

    {
        brand_id: 2,
        brand_name: "Nutrience"
    },

    {
        brand_id: 3,
        brand_name: "PureVita"
    },

    {
        brand_id: 4,
        brand_name: "Genérico"
    }
];


/* ==========================================================================
   CATEGORÍAS
   ========================================================================== */

export const MOCK_CATEGORIES = [
    {
        category_id: 1,
        category_name: "Alimento para Perros"
    },

    {
        category_id: 2,
        category_name: "Alimento para Gatos"
    },

    {
        category_id: 3,
        category_name: "Accesorios"
    }
];


/* ==========================================================================
   PRODUCTOS INICIALES
   ========================================================================== */

const INITIAL_MOCK_PRODUCTS = [

    {
        product_id: 1,
        name: "Alimento Seco para Cachorros",
        price: 24.99,
        quantity: 15,
        brand: "NutriSource",
        category: "Alimento para Perros",
        image: "img/products/food-1.jpg"
    },

    {
        product_id: 2,
        name: "Alimento Húmedo Sabor Mariscos",
        price: 8.5,
        quantity: 30,
        brand: "NutriSource",
        category: "Alimento para Perros",
        image: "img/products/food-2.jpg"
    },

    {
        product_id: 3,
        name: "Alimento Seco para Gatos Adultos",
        price: 19.99,
        quantity: 0,
        brand: "Nutrience",
        category: "Alimento para Gatos",
        image: "img/products/food-3.jpg"
    },

    {
        product_id: 4,
        name: "Arnés Ajustable Talla M",
        price: 12.0,
        quantity: 8,
        brand: "Genérico",
        category: "Accesorios",
        image: "img/products/img-3.jpg"
    },

    {
        product_id: 5,
        name: "Alimento Limitado Pollo y Arvejas",
        price: 22.5,
        quantity: 5,
        brand: "PureVita",
        category: "Alimento para Gatos",
        image: "img/products/food-4.jpg"
    },

    {
        product_id: 6,
        name: "Bowl de alimento para gatos",
        price: 7.0,
        quantity: 18,
        brand: "Genérico",
        category: "Accesorios",
        image: "img/products/img-5.jpg"
    },

    {
        product_id: 7,
        name: "Hueso navideño de juguete para perros medianos",
        price: 10.0,
        quantity: 3,
        brand: "Genérico",
        category: "Accesorios",
        image: "img/products/img-4.jpg"
    },

    {
        product_id: 8,
        name: "Rascador portátil para Gato",
        price: 15.0,
        quantity: 2,
        brand: "Genérico",
        category: "Accesorios",
        image: "img/products/img-6.jpg"
    }

];


/* ==========================================================================
   PERSISTENCIA DEL INVENTARIO
   ========================================================================== */

const MOCK_PRODUCTS_KEY =
    "valespetstore_mock_products_v2";


function getLocalProducts() {

    try {

        const raw =
            localStorage.getItem(
                MOCK_PRODUCTS_KEY
            );


        if (!raw) {
            return null;
        }


        const products =
            JSON.parse(raw);


        if (!Array.isArray(products)) {
            return null;
        }


        return products;

    } catch (error) {

        console.error(
            "No se pudo leer el inventario local:",
            error
        );

        return null;
    }
}


function saveLocalProducts(products) {

    localStorage.setItem(
        MOCK_PRODUCTS_KEY,
        JSON.stringify(products)
    );
}


/*
 * Si ya existen productos guardados,
 * utilizamos esos.
 *
 * Si es la primera vez,
 * cargamos los 8 productos iniciales.
 */

const savedProducts =
    getLocalProducts();


let mockProducts =
    savedProducts ||
    INITIAL_MOCK_PRODUCTS.map(
        (product) => ({
            ...product
        })
    );


/*
 * Guardamos el inventario inicial.
 */

if (!savedProducts) {

    saveLocalProducts(
        mockProducts
    );
}


/*
 * El próximo ID siempre será mayor
 * que el ID más alto existente.
 */

let nextProductId =
    mockProducts.reduce(
        (max, product) =>
            Math.max(
                max,
                Number(product.product_id) || 0
            ),
        0
    ) + 1;


/* ==========================================================================
   CARRITO
   ========================================================================== */

let mockCartItems =
    getLocalCartItems();


let nextCartItemId =
    mockCartItems.reduce(
        (max, item) =>
            Math.max(
                max,
                Number(item.cart_item_id) || 0
            ),
        0
    ) + 1;


/* ==========================================================================
   PEDIDOS
   ========================================================================== */

let mockOrders = [

    {
        order_id: 1001,
        customer_id: 1,
        order_date: "2026-09-10T14:00:00",
        total_amount: 41.48,
        status: "completed"
    }

];


let nextOrderId = 1002;


const mockInvoices = {};


/* ==========================================================================
   FUNCIONES DEL CARRITO
   ========================================================================== */

function cartTotal() {

    return mockCartItems.reduce(
        (sum, item) =>
            sum +
            Number(item.subtotal || 0),
        0
    );
}


/* ==========================================================================
   AUTH
   ========================================================================== */

export async function mockRegister() {

    await delay();


    return {
        userId:
            Math.floor(
                Math.random() * 1000
            ),

        customerId: 1
    };
}


export async function mockLogin({ email }) {

    await delay();


    const role =
        email
            .trim()
            .toLowerCase() ===
            MOCK_ADMIN_EMAIL
            ? "admin"
            : "user";


    return {
        message: "Login successful",

        token: "mock-token",

        role,

        customer_id: 1
    };
}


/* ==========================================================================
   PRODUCTOS
   ========================================================================== */

export async function mockGetProducts() {

    await delay();


    return mockProducts;
}


export async function mockGetProductById(id) {

    await delay();


    const product =
        mockProducts.find(
            (p) =>
                String(p.product_id) ===
                String(id)
        );


    if (!product) {

        throw new Error(
            "Producto no encontrado."
        );
    }


    return product;
}


export async function mockGetBrands() {

    await delay(150);

    return MOCK_BRANDS;
}


export async function mockGetCategories() {

    await delay(150);

    return MOCK_CATEGORIES;
}


/* ==========================================================================
   CARRITO
   ========================================================================== */

export async function mockAddItemToCart(
    productId,
    quantity
) {

    await delay();


    const product =
        mockProducts.find(
            (p) =>
                Number(p.product_id) ===
                Number(productId)
        );


    if (!product) {

        throw new Error(
            "Producto no encontrado."
        );
    }


    if (
        Number(product.quantity) <= 0
    ) {

        throw new Error(
            "Este producto está agotado."
        );
    }


    const requestedQuantity =
        Number(quantity);


    if (
        requestedQuantity <= 0
    ) {

        throw new Error(
            "La cantidad debe ser mayor que cero."
        );
    }


    const existing =
        mockCartItems.find(
            (item) =>
                Number(item.product_id) ===
                Number(productId)
        );


    const currentQuantity =
        existing
            ? Number(existing.quantity)
            : 0;


    if (
        currentQuantity +
        requestedQuantity >
        Number(product.quantity)
    ) {

        throw new Error(
            `Solo hay ${product.quantity} unidades disponibles.`
        );
    }


    if (existing) {

        existing.quantity +=
            requestedQuantity;

        existing.subtotal =
            existing.quantity *
            existing.unit_price;

    } else {

        mockCartItems.push({

            cart_item_id:
                nextCartItemId++,

            product_id:
                product.product_id,

            product_name:
                product.name,

            unit_price:
                Number(product.price),

            quantity:
                requestedQuantity,

            subtotal:
                Number(product.price) *
                requestedQuantity

        });
    }


    saveLocalCartItems(
        mockCartItems
    );


    window.dispatchEvent(
        new CustomEvent(
            "cart-updated"
        )
    );


    return {
        message: "Item added"
    };
}


export async function mockGetCart() {

    await delay(200);


    return {

        cart_id: 1,

        customer_id: 1,

        items: mockCartItems,

        total: cartTotal()

    };
}


export async function mockRemoveItemFromCart(
    itemId
) {

    await delay(200);


    mockCartItems =
        mockCartItems.filter(
            (item) =>
                String(item.cart_item_id) !==
                String(itemId)
        );


    saveLocalCartItems(
        mockCartItems
    );


    window.dispatchEvent(
        new CustomEvent(
            "cart-updated"
        )
    );


    return {
        message: "Item removed"
    };
}


/* ==========================================================================
   CHECKOUT
   ========================================================================== */

export async function mockCheckout({
    billingAddress,
    paymentMethod
}) {

    await delay(500);


    if (
        mockCartItems.length === 0
    ) {

        throw new Error(
            "El carrito está vacío."
        );
    }


    /*
     * Verificar nuevamente el stock
     * antes de crear el pedido.
     */

    for (const item of mockCartItems) {

        const product =
            mockProducts.find(
                (p) =>
                    Number(p.product_id) ===
                    Number(item.product_id)
            );


        if (!product) {

            throw new Error(
                `El producto "${item.product_name}" ya no existe.`
            );
        }


        if (
            Number(item.quantity) >
            Number(product.quantity)
        ) {

            throw new Error(
                `No hay suficiente stock de "${product.name}".`
            );
        }
    }


    const orderId =
        nextOrderId++;


    const items =
        mockCartItems.map(
            (item) => ({
                ...item
            })
        );


    const total =
        cartTotal();


    /*
     * Descontar productos del inventario.
     */

    for (const item of mockCartItems) {

        const product =
            mockProducts.find(
                (p) =>
                    Number(p.product_id) ===
                    Number(item.product_id)
            );


        if (product) {

            product.quantity =
                Number(product.quantity) -
                Number(item.quantity);
        }
    }


    /*
     * Guardar nuevo stock.
     */

    saveLocalProducts(
        mockProducts
    );


    /*
     * Crear pedido.
     */

    mockOrders.unshift({

        order_id:
            orderId,

        customer_id:
            1,

        order_date:
            new Date().toISOString(),

        total_amount:
            total,

        status:
            "completed"

    });


    /*
     * Crear factura.
     */

    mockInvoices[orderId] = {

        order_id:
            orderId,

        order_date:
            new Date().toISOString(),

        items,

        total_amount:
            total,

        billing_address:
            billingAddress,

        payment_method:
            paymentMethod

    };


    /*
     * Vaciar carrito.
     */

    mockCartItems = [];


    clearLocalCartItems();


    window.dispatchEvent(
        new CustomEvent(
            "cart-updated"
        )
    );


    return {

        message:
            "Order created",

        order_id:
            orderId,

        total_amount:
            total,

        billing_address:
            billingAddress,

        payment_method:
            paymentMethod

    };
}
/* ==========================================================================
   FACTURAS
   ========================================================================== */

export async function mockGetInvoice(
    orderId
) {

    await delay(250);


    const invoice =
        mockInvoices[orderId];


    if (!invoice) {

        throw new Error(
            "Factura no encontrada."
        );
    }


    return invoice;
}

/* ==========================================================================
   ADMINISTRACIÓN
   ========================================================================== */
/* --------------------------------------------------------------------------
   Crear producto
   -------------------------------------------------------------------------- */

export async function mockCreateProduct({
    name,
    price,
    quantity,
    brandId,
    categoryId,
    image
}) {
    await delay();


    const brand =
        MOCK_BRANDS.find(
            (b) =>
                Number(b.brand_id) ===
                Number(brandId)
        );


    const category =
        MOCK_CATEGORIES.find(
            (c) =>
                Number(c.category_id) ===
                Number(categoryId)
        );


    const newName =
        String(name || "").trim();


    const newPrice =
        Number(price);


    const newQuantity =
        Number(quantity);


    if (!newName) {

        throw new Error(
            "El nombre del producto es obligatorio."
        );
    }


    if (
        !Number.isFinite(newPrice) ||
        newPrice < 0
    ) {

        throw new Error(
            "El precio no es válido."
        );
    }


    if (
        !Number.isFinite(newQuantity) ||
        newQuantity < 0
    ) {

        throw new Error(
            "El stock no es válido."
        );
    }


    /*
     * Si el administrador seleccionó una imagen,
     * se guarda como Data URL.
     *
     * Si no seleccionó ninguna,
     * utilizamos la imagen predeterminada.
     */

    const productImage =
        typeof image === "string" &&
            image.trim() !== ""
            ? image
            : "img/products/img-1.jpg";


    const product = {

        product_id:
            nextProductId++,

        name:
            newName,

        price:
            newPrice,

        quantity:
            newQuantity,

        brand:
            brand?.brand_name ||
            "Genérico",

        category:
            category?.category_name ||
            "General",

        image:
            productImage
    };


    mockProducts.push(
        product
    );


    saveLocalProducts(
        mockProducts
    );


    return {

        message:
            "Product created",

        product_id:
            product.product_id
    };
}


/* --------------------------------------------------------------------------
   Editar producto
   -------------------------------------------------------------------------- */

export async function mockUpdateProduct(
    id,
    {
        name,
        price,
        quantity,
        brandId,
        categoryId,
        image
    }
) {

    await delay();


    const product =
        mockProducts.find(
            (p) =>
                String(p.product_id) ===
                String(id)
        );


    if (!product) {

        throw new Error(
            "Producto no encontrado."
        );
    }


    const newName =
        String(name || "").trim();


    const newPrice =
        Number(price);


    const newQuantity =
        Number(quantity);


    if (!newName) {

        throw new Error(
            "El nombre del producto es obligatorio."
        );
    }


    if (
        !Number.isFinite(newPrice) ||
        newPrice < 0
    ) {

        throw new Error(
            "El precio no es válido."
        );
    }


    if (
        !Number.isFinite(newQuantity) ||
        newQuantity < 0
    ) {

        throw new Error(
            "El stock no es válido."
        );
    }


    const brand =
        MOCK_BRANDS.find(
            (b) =>
                Number(b.brand_id) ===
                Number(brandId)
        );


    const category =
        MOCK_CATEGORIES.find(
            (c) =>
                Number(c.category_id) ===
                Number(categoryId)
        );


    /*
     * Actualizar información.
     */

    product.name =
        newName;


    product.price =
        newPrice;


    product.quantity =
        newQuantity;


    if (brand) {

        product.brand =
            brand.brand_name;
    }


    if (category) {

        product.category =
            category.category_name;
    }


    /*
     * IMPORTANTE:
     *
     * Si llega una nueva imagen,
     * reemplazamos la anterior.
     *
     * Si image está vacío,
     * conservamos la imagen existente.
     */

    if (
        typeof image === "string" &&
        image.trim() !== ""
    ) {

        product.image =
            image;
    }


    /*
     * Si por alguna razón el producto
     * todavía no tiene imagen,
     * colocar una predeterminada.
     */

    if (
        typeof product.image !== "string" ||
        product.image.trim() === ""
    ) {

        product.image =
            "img/products/img-1.jpg";
    }


    saveLocalProducts(
        mockProducts
    );


    return {

        message:
            "Product updated"
    };
}


/* --------------------------------------------------------------------------
   Eliminar producto
   -------------------------------------------------------------------------- */

export async function mockDeleteProduct(
    id
) {

    await delay();


    const exists =
        mockProducts.some(
            (p) =>
                String(p.product_id) ===
                String(id)
        );


    if (!exists) {

        throw new Error(
            "Producto no encontrado."
        );
    }


    mockProducts =
        mockProducts.filter(
            (p) =>
                String(p.product_id) !==
                String(id)
        );


    saveLocalProducts(
        mockProducts
    );


    return {
        message:
            "Product deleted"
    };
}


/* --------------------------------------------------------------------------
   Obtener pedidos
   -------------------------------------------------------------------------- */

export async function mockGetOrders() {

    await delay();


    return mockOrders;
}


/* --------------------------------------------------------------------------
   Reembolsar pedido
   -------------------------------------------------------------------------- */

export async function mockRefundOrder(
    orderId
) {

    await delay();


    const order =
        mockOrders.find(
            (o) =>
                String(o.order_id) ===
                String(orderId)
        );


    if (!order) {

        throw new Error(
            "Pedido no encontrado."
        );
    }


    order.status =
        "refunded";


    return {
        message:
            "Order refunded"
    };
}
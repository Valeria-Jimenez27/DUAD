import {
    apiFetch,
    USE_MOCK_DATA
} from "./config.js";

import {
    mockCreateProduct,
    mockUpdateProduct,
    mockDeleteProduct,
    mockGetOrders,
    mockRefundOrder
} from "./mockData.js";


export async function createProduct({
    name,
    price,
    quantity,
    brandId,
    categoryId,
    image
}) {

    if (USE_MOCK_DATA) {

        return mockCreateProduct({
            name,
            price,
            quantity,
            brandId,
            categoryId,
            image
        });
    }


    return apiFetch(
        "/products",
        {
            method: "POST",

            body: {
                name,
                price,
                quantity,
                brand_id: brandId,
                category_id: categoryId,
                image
            }
        }
    );
}


export async function updateProduct(
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

    if (USE_MOCK_DATA) {

        return mockUpdateProduct(
            id,
            {
                name,
                price,
                quantity,
                brandId,
                categoryId,
                image
            }
        );
    }


    return apiFetch(
        `/products/${id}`,
        {
            method: "PUT",

            body: {
                name,
                price,
                quantity,
                brand_id: brandId,
                category_id: categoryId,
                image
            }
        }
    );
}


export async function deleteProduct(
    id
) {

    if (USE_MOCK_DATA) {
        return mockDeleteProduct(id);
    }

    return apiFetch(
        `/products/${id}`,
        {
            method: "DELETE"
        }
    );
}


export async function getOrders() {

    if (USE_MOCK_DATA) {
        return mockGetOrders();
    }

    return apiFetch(
        "/orders",
        {
            method: "GET"
        }
    );
}


export async function refundOrder(
    orderId
) {

    if (USE_MOCK_DATA) {
        return mockRefundOrder(
            orderId
        );
    }

    return apiFetch(
        `/orders/${orderId}/refund`,
        {
            method: "POST"
        }
    );
}
/*
 * ==========================================================================
 * purchase-complete.js — Lógica de la página purchase-complete.html.
 * ==========================================================================
 */

import { getInvoice } from "./orderService.js";

import { isLoggedIn } from "./storage.js";

import {
    showAlert,
    renderAccessRestricted,
    escapeHtml
} from "./ui.js";

const loadingEl = document.getElementById("invoice-loading");
const contentEl = document.getElementById("invoice-content");
const apiErrorEl = document.getElementById("api-error");

const orderIdEl = document.getElementById("order-id");
const orderDateEl = document.getElementById("order-date");
const itemsEl = document.getElementById("invoice-items");
const totalEl = document.getElementById("invoice-total");
const addressEl = document.getElementById("invoice-address");
const paymentEl = document.getElementById("invoice-payment");

const PAYMENT_LABELS = {
    tarjeta: "Tarjeta de crédito/débito",
    sinpe: "SINPE Móvil",
    efectivo: "Efectivo contra entrega"
};

if (!isLoggedIn()) {
    document.getElementById("page-content").hidden = true;

    renderAccessRestricted(
        document.getElementById("access-restricted"),
        {
            title: "Debes iniciar sesión para continuar",
            message:
                "Inicia sesión para ver el comprobante de tu compra.",
            buttonText: "Ir a iniciar sesión",
            buttonHref: "login.html"
        }
    );
}

const params = new URLSearchParams(window.location.search);
const orderId = params.get("order_id");

function renderInvoice(invoice) {
    const invoiceOrderId = Number(invoice.order_id);

    orderIdEl.textContent = `#${invoiceOrderId}`;

    orderDateEl.textContent =
        new Date(invoice.order_date).toLocaleDateString(
            "es-CR",
            {
                year: "numeric",
                month: "long",
                day: "numeric"
            }
        );

    itemsEl.innerHTML =
        invoice.items
            .map((item) => {
                const productName =
                    item.product_name || "Producto";

                const quantity =
                    Number(item.quantity || 0);

                const unitPrice =
                    Number(item.unit_price || 0);

                const subtotal =
                    Number(item.subtotal || 0);

                return `
                    <tr>
                        <td>
                            ${escapeHtml(productName)}
                        </td>
                        <td>
                            ${quantity}
                        </td>
                        <td>
                            $${unitPrice.toFixed(2)}
                        </td>
                        <td>
                            $${subtotal.toFixed(2)}
                        </td>
                    </tr>
                `;
            })
            .join("");

    totalEl.textContent =
        `$${Number(invoice.total_amount || 0).toFixed(2)}`;

    addressEl.textContent =
        invoice.billing_address || "";

    paymentEl.textContent =
        PAYMENT_LABELS[invoice.payment_method] ||
        invoice.payment_method ||
        "";

    loadingEl.hidden = true;
    contentEl.hidden = false;
}

async function loadInvoice() {
    if (!orderId) {
        loadingEl.hidden = true;

        showAlert(
            apiErrorEl,
            "No se especificó ningún pedido.",
            "error"
        );

        return;
    }

    try {
        const invoice = await getInvoice(orderId);

        renderInvoice(invoice);
    } catch (error) {
        loadingEl.hidden = true;

        showAlert(
            apiErrorEl,
            error.message,
            "error"
        );
    }
}

if (isLoggedIn()) {
    loadInvoice();
}
# Vale's Pet Store — Frontend

**Project:** `Proyecto_final_de_modulo2_frontend`

Vale's Pet Store is the frontend for the PetStore application. Customers can create an account, sign in, browse products, manage a shopping cart, complete checkout, and view an invoice. Administrators can manage products, review orders, and request refunds.

The application is built with **HTML5, CSS3, and vanilla JavaScript using ES modules**. It does not require `npm`, a JavaScript framework, or a build step.

> **Current configuration:** the frontend is configured to use the real backend API. In `js/config.js`, `USE_MOCK_DATA` should remain `false` for the project demonstration.

---

## Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Run the application](#run-the-application)
- [Customer and administrator flows](#customer-and-administrator-flows)
- [Project structure](#project-structure)
- [Pages and access](#pages-and-access)
- [Architecture](#architecture)
- [Technology stack](#technology-stack)
- [Authentication and session storage](#authentication-and-session-storage)
- [Backend integration](#backend-integration)
- [API operations used by the frontend](#api-operations-used-by-the-frontend)
- [Data expected by the interface](#data-expected-by-the-interface)
- [Error handling](#error-handling)
- [Technical decisions](#technical-decisions)
- [Known considerations](#known-considerations)
- [Troubleshooting](#troubleshooting)
- [Before the demonstration](#before-the-demonstration)

---

## Prerequisites

- A modern browser: Chrome, Edge, Firefox, or Safari.
- Python 3 or the VS Code **Live Server** extension to serve the frontend over HTTP.
- The backend API running at `http://127.0.0.1:5000`, unless `API_BASE_URL` has been changed.
- The backend's required services and database configured according to the backend project's own README.
- Internet access is needed to load Google Fonts (Baloo 2 and Nunito Sans). If they are unavailable, the browser uses fallback fonts.

> Do not open the HTML files by double-clicking them. ES modules and browser requests should be tested through an HTTP server, not a `file://` URL.

---

## Installation

Clone the repository and enter the frontend folder:

```bash
git clone https://github.com/Valeria-Jimenez27/DUAD.git
cd DUAD/Proyecto_final_de_modulo2_frontend
```

There are no frontend packages to install. The project does not use `package.json` or a build command.

---

## Configuration

Frontend configuration is centralized in `js/config.js`.

| Setting | Current value | Purpose |
|---|---|---|
| `USE_MOCK_DATA` | `false` | Uses the real API when set to `false`; uses simulated data when set to `true`. |
| `API_BASE_URL` | `http://127.0.0.1:5000` | Base URL for backend requests. |

For the project demonstration, use the address where the backend is actually running. If the backend uses a different host or port, update `API_BASE_URL`.

The frontend does not contain backend secrets. Anything included in frontend code is delivered to the browser and must be treated as public.

---

## Run the application

### 1. Start the backend

Start the Flask backend using the instructions in the backend project's README. In the current local setup, the API base URL is:

```text
http://127.0.0.1:5000
```

Keep the backend terminal running while testing the frontend.

### 2. Start the frontend

From the frontend project directory, run:

```bash
python -m http.server 8080
```

Alternatively, use the Live Server extension in Visual Studio Code.

### 3. Open the application

With Python's server, open:

```text
http://localhost:8080
```

The frontend and backend use different origins when served this way. If the browser console reports a CORS error, configure the backend to allow the exact frontend origin, including its host and port. Do not change CORS settings unless needed; verify the browser console and backend configuration first.

### 4. Sign in

Use an account that exists in the backend. Demo-mode accounts are only relevant when `USE_MOCK_DATA` is set to `true`; they are not valid real API accounts unless the same accounts also exist in the backend database.

---

## Customer and administrator flows

### Customer flow

1. `register.html` — create a customer account.
2. `login.html` — sign in.
3. `catalog.html` — browse, search, and filter products.
4. `product.html?id=...` — view a product's details and add it to the cart.
5. `cart.html` — review or remove cart items.
6. `order-summary.html` — enter the billing address and choose a payment method.
7. `purchase-complete.html?order_id=...` — view the invoice for the completed order.

The supported payment method values sent by the frontend are `tarjeta`, `sinpe`, and `efectivo`.

### Administrator flow

1. Sign in with an administrator account.
2. Open `admin-panel.html`.
3. Use the inventory area to create, edit, or delete products.
4. Use the sales area to review orders and request refunds.
5. Use `edit-product.html` to create a product or edit an existing product with `?id=...`.

The backend must enforce administrator permissions. Hiding an admin page in the frontend is not a security boundary.

---

## Project structure

```text
Proyecto_final_de_modulo2_frontend/
│
├── index.html                 # Home page
├── login.html                 # Sign in
├── register.html              # Customer registration
├── catalog.html               # Product catalog and filters
├── product.html               # Product details (?id=)
├── cart.html                  # Shopping cart
├── order-summary.html         # Billing address and payment
├── purchase-complete.html     # Invoice (?order_id=)
├── admin-panel.html           # Product inventory and sales
├── edit-product.html          # Create/edit product (?id= to edit)
│
├── css/
│   ├── variables.css          # Design tokens: colors, typography, spacing
│   ├── base.css               # Reset and global styles
│   ├── layout.css             # Header, containers, grids
│   └── components.css         # Buttons, cards, forms, tables, alerts
│
├── js/
│   ├── config.js              # API_BASE_URL, USE_MOCK_DATA, apiFetch(), ApiError
│   ├── storage.js             # Session, customer, cart identifiers, mock cart storage
│   ├── authService.js         # Registration and login requests
│   ├── productService.js      # Product, brand, and category requests
│   ├── orderService.js        # Cart, checkout, and invoice requests
│   ├── adminService.js        # Product administration, orders, refunds
│   ├── mockData.js             # Simulated data for demo mode
│   ├── validators.js          # Reusable form validation
│   ├── ui.js                  # Alerts, field errors, loading, restricted-access UI
│   ├── productImage.js        # Product image selection
│   ├── header.js              # Shared header behavior
│   └── [page].js              # JavaScript module for each page
│
└── img/
    └── products/              # Logo and product images
```

Each HTML page loads the shared stylesheets and `js/header.js`, along with its own page script, using `type="module"`.

---

## Pages and access

| Page | Access | Main script | Main operations |
|---|---|---|---|
| `index.html` | Public | `index.js` | Home page and category/product presentation |
| `login.html` | Public | `login.js` | Sign in |
| `register.html` | Public | `register.js` | Registration and sign-in |
| `catalog.html` | Signed-in user | `catalog.js` | Browse products and add items to cart |
| `product.html` | Signed-in user | `product.js` | Product details and add to cart |
| `cart.html` | Signed-in user | `cart.js` | View and remove cart items |
| `order-summary.html` | Signed-in user | `orderSummary.js` | Review cart and complete checkout |
| `purchase-complete.html` | Signed-in user | `purchaseComplete.js` | Retrieve and display invoice |
| `admin-panel.html` | Administrator | `adminPanel.js` | Inventory and sales administration |
| `edit-product.html` | Administrator | `editProduct.js` | Create or update a product |

Page-to-page state is passed through URL parameters such as `?id=`, `?order_id=`, `?search=`, and `?category=`, or through `localStorage` for the session and cart identifier.

---

## Architecture

The frontend separates page behavior, service calls, and shared utilities:

```text
HTML page
   |
   v
Page JavaScript module
(DOM, events, display states)
   |
   v
Service module
(API operation or mock implementation)
   |
   v
apiFetch() ------------------> Backend REST API
   |
   +---- mock implementation when USE_MOCK_DATA is true
```

- Page scripts handle DOM events and render loading, empty, success, and error states.
- Service modules centralize operations such as authentication, products, carts, checkout, invoices, and administration.
- `apiFetch()` centralizes HTTP requests, JSON serialization, authorization headers, and API error handling.
- `storage.js` centralizes access to session and cart identifiers in `localStorage`.
- `validators.js` contains reusable validation rules.
- `ui.js` contains reusable interface helpers, including alerts and restricted-access messages.
- `mockData.js` supplies simulated data only when demo mode is enabled.

---

## Technology stack

| Technology | Purpose |
|---|---|
| HTML5 | Multi-page structure and semantic markup |
| CSS3 | Responsive layout, design variables, and component styling |
| JavaScript ES modules | Page logic and modular service layer |
| Fetch API | HTTP communication with the backend |
| `localStorage` | Session values, cart identifier, and demo data |
| Google Fonts | Baloo 2 headings and Nunito Sans body text |
| Flask REST API | Authentication, products, carts, orders, and invoices |
| PostgreSQL and Redis | Backend data and caching, configured in the backend project |

---

## Authentication and session storage

The frontend stores the authentication information returned by the backend and sends the token with protected API requests.

1. After successful sign-in, `authService.js` saves session values using `storage.js`.
2. `apiFetch()` adds an `Authorization: Bearer <token>` header when authentication is required and a token is available.
3. Pages use client-side checks to decide whether to display protected content.
4. Signing out clears the frontend session values and returns the user to the home page.

The application uses these storage keys:

| Key | Purpose |
|---|---|
| `petstore_token` | Authentication token |
| `petstore_role` | Role used by the frontend to select the appropriate interface |
| `petstore_user_name` | Display name, when available |
| `petstore_customer_id` | Customer identifier associated with the account |
| `petstore_cart_id` | Cart identifier used by the real API |
| `petstore_mock_cart_items` | Cart items for demo mode |
| `valespetstore_mock_products_v2` | Simulated product data, when used by the mock implementation |

Client-side access checks are for user experience only. They can be changed in the browser and must not replace authorization checks on the backend.

The token is stored in `localStorage`, which is convenient for this multi-page project but can expose the token if a cross-site scripting (XSS) vulnerability exists. Production systems should evaluate safer session designs and additional security controls.

---

## Backend integration

The frontend connects to the Flask API project `Proyecto_final_de_modulo2`.

### API base URL

The current local API address is configured in `js/config.js`:

```js
export const API_BASE_URL = "http://127.0.0.1:5000";
export const USE_MOCK_DATA = false;
```

Set `USE_MOCK_DATA` to `false` when demonstrating the application with the real API. Change `API_BASE_URL` if the API is running at another address.

### Authentication

Protected requests use a Bearer token:

```http
Authorization: Bearer <token>
```

Sign in through the frontend to store the token before testing protected operations. Calling protected endpoints directly without a token may return an error such as `Token missing`.

### CORS

When the frontend and backend are served from different origins, the backend must allow the frontend origin. An origin includes the scheme, hostname, and port; for example, `http://localhost:8080` and `http://127.0.0.1:8080` are different origins.

If the browser reports a CORS error, configure CORS in the backend for the origin actually used to open the frontend. CORS is a backend configuration, not a frontend setting.

### Demo mode

To use simulated data for isolated frontend demonstrations, set:

```js
export const USE_MOCK_DATA = true;
```

Demo mode is not the configuration for the real-backend demonstration. Mock behavior and persisted mock data may differ from the backend's actual data and business rules.

---

## API operations used by the frontend

The following table documents the operations used by the frontend service layer. The API must be running, and protected requests require a valid token. Confirm exact request and response details against the backend implementation if either project changes.

| Frontend operation | HTTP request | Purpose |
|---|---|---|
| `register()` | `POST /register` | Register an account |
| `login()` | `POST /login` | Authenticate and obtain a token |
| `getProducts()` | `GET /products` | Retrieve products |
| `getProductById(id)` | `GET /products/{id}` | Retrieve one product |
| `getBrands()` | `GET /brands` | Retrieve brands for product forms |
| `getCategories()` | `GET /categories` | Retrieve categories for product forms |
| `getOrCreateCart()` | `POST /carts` with `customer_id` | Create a cart when needed |
| `getCart(cartId)` | `GET /carts/{cart_id}` | Retrieve cart contents |
| `addItemToCart()` | `POST /carts/{cart_id}/items` with `product_id` and `quantity` | Add an item |
| `removeItemFromCart()` | `DELETE /carts/{cart_id}/items/{item_id}` | Remove an item |
| `checkout()` | `POST /carts/{cart_id}/checkout` with `billing_address` and `payment_method` | Complete a purchase |
| `getInvoice(orderId)` | `GET /orders/{order_id}/invoice` | Retrieve an invoice |
| `createProduct()` | `POST /products` | Create a product |
| `updateProduct(id)` | `PUT /products/{id}` | Update a product |
| `deleteProduct(id)` | `DELETE /products/{id}` | Delete a product |
| `getOrders()` | `GET /orders` | Retrieve orders for the sales view |
| `refundOrder(orderId)` | `POST /orders/{order_id}/refund` | Request an order refund |

Authentication and authorization requirements are ultimately determined by the backend. Some lookup endpoints may be public while others require a token.

---

## Data expected by the interface

The page scripts rely on response fields such as the following. If the backend response shape changes, update the relevant service or page code and keep the mock implementation aligned if demo mode is still supported.

| Resource | Fields used by the frontend |
|---|---|
| Product | `product_id`, `name`, `price`, `quantity`, `brand`, `category` |
| Brand | `brand_id`, `brand_name` |
| Category | `category_id`, `category_name` |
| Cart | `items`, `total` |
| Cart item | `cart_item_id`, `product_id`, `product_name`, `unit_price`, `quantity`, `subtotal` |
| Checkout result | `order_id` |
| Invoice | `order_id`, `order_date`, `items`, `total_amount`, `billing_address`, `payment_method` |
| Order | `order_id`, `customer_id`, `order_date`, `total_amount`, `status` |
| Login result | `token`, `role`, and the customer identifier when returned |
| API error | An error message, commonly in an `error` field |

The exact response shape is defined by the backend. If a value is missing or named differently, inspect the network response and update the relevant service mapping rather than assuming the field exists.

---

## Error handling

`apiFetch()` is the shared HTTP request helper. It serializes request bodies as JSON, sends the authorization header when required, parses JSON responses, and throws an `ApiError` for failed requests.

Typical issues include:

- **Connection failure:** the backend is stopped or `API_BASE_URL` is incorrect.
- **Authentication failure:** the token is missing, invalid, or expired.
- **Authorization failure:** the current account does not have permission for the operation.
- **Validation failure:** required data is missing or does not meet the backend's rules.
- **CORS failure:** the backend does not allow the origin used by the frontend.

Page scripts catch request errors and display a message in the page's alert area. The API remains the authority for business rules, stock, and permissions.

---

## Technical decisions

### 1. Vanilla HTML, CSS, and JavaScript

The project demonstrates core frontend concepts without a framework, bundler, or dependency installation. The trade-off is that DOM rendering and shared markup require more manual maintenance.

### 2. Multi-page structure

Each screen has its own HTML page and JavaScript module. This makes each feature easy to locate, but navigation reloads the page. Session and cart identifiers are therefore stored between page loads.

### 3. ES modules

Imports and exports make dependencies explicit and keep code organized by responsibility. The application must be served through HTTP for modules to load reliably.

### 4. Service layer and shared request helper

Service modules separate API operations from page presentation. `apiFetch()` centralizes headers, JSON handling, and errors so request behavior is consistent.

### 5. Optional demo mode

`USE_MOCK_DATA` supports simulated data for frontend development. Mock data should be kept consistent with the API, but the real-backend demonstration should use `USE_MOCK_DATA = false`.

### 6. Token storage

The token is stored in `localStorage` to persist across page navigation. This is simple for a learning project but requires careful attention to XSS prevention; frontend role checks do not secure backend resources.

### 7. Client-side form validation

Reusable validation functions provide immediate feedback. The backend must validate submitted data independently because client-side validation can be bypassed.

### 8. Client-side catalog filtering

The frontend filters the loaded product list in the browser. This is appropriate for a small catalog; larger catalogs may require server-side filtering and pagination.

### 9. Product image mapping

The API product model may not provide an image path. `productImage.js` selects an image using the available product information and configured image mapping. Keep the mapping aligned with the product data and the actual files in `img/products/`.

### 10. Layered CSS

Styles are split into variables, base styles, layout, and components. This keeps design tokens and shared presentation rules in predictable locations.

### 11. Explicit interface states

Pages provide loading, empty, error, and restricted-access states where applicable. Buttons are disabled during some asynchronous operations to reduce accidental repeated submissions.

### 12. Spanish interface

The interface is designed for a Costa Rican audience, including SINPE Móvil as a payment option. Code identifiers are primarily in English while user-facing text is in Spanish.

---

## Known considerations

The following are items to verify during testing; they should not be treated as confirmed failures without reproducing them in the current version.

1. **Cart counter in real mode:** verify that the shared header displays the correct count after adding or removing items when using the real API.
2. **Product images:** verify that every product currently returned by the API has a valid image mapping or a working fallback image.
3. **Home page without a session:** verify that public home-page content loads correctly for signed-out visitors. Public content should not depend on an endpoint that requires authentication.
4. **Displayed user name:** verify whether the login response provides a name. If it does not, the header may display the email instead.
5. **Category icons:** verify that icon selection matches the category names returned by the backend.
6. **Dynamic HTML:** any values received from the API and inserted into `innerHTML` must be escaped or rendered safely to prevent HTML injection and possible XSS.
7. **Expired sessions:** verify how the interface responds when the token expires. Users may need to sign in again.
8. **Demo invoices:** mock orders and invoices may have different persistence behavior from real backend orders. Test invoice retrieval with the real API for the project demonstration.

If an issue is reproduced, update this section to record the actual behavior and the implemented fix.

---

## Troubleshooting

| Symptom | Possible cause | What to check |
|---|---|---|
| JavaScript module errors or pages do not load correctly | The HTML page was opened with `file://` | Start an HTTP server and open the `http://localhost:8080` address |
| "No se pudo conectar con el servidor" | Backend is stopped or API URL is wrong | Check that Flask is running and `API_BASE_URL` matches its address |
| Browser console reports a CORS error | Backend does not allow the frontend origin | Allow the exact origin and port in the backend CORS configuration |
| `Token missing` | The request did not include an authentication token | Sign in through the frontend and retry the protected operation |
| Invalid or expired token | The session token is no longer valid | Sign in again |
| Product or cart request returns an error | The request may be unauthorized, the identifier may be invalid, or the backend may reject the data | Inspect the Network tab and the backend terminal for the response details |
| Product image is broken | The image path or product image mapping does not match an existing file | Check `js/productImage.js` and the contents of `img/products/` |
| Demo data looks outdated | Browser storage contains mock data from an earlier run | In demo mode only, clear the relevant application keys from DevTools → Application → Local Storage |
| Invoice is not displayed | The order ID may be missing or the API may not return the expected invoice structure | Check the `order_id` URL parameter and the invoice request in the Network tab |

Use browser DevTools (Console, Network, and Application/Local Storage) alongside the backend terminal when diagnosing a failure.

---

## Before the demonstration

- [ ] The backend and its required services are running.
- [ ] `USE_MOCK_DATA = false` in `js/config.js`.
- [ ] `API_BASE_URL` points to the running backend.
- [ ] The frontend is served over HTTP.
- [ ] The browser console has no blocking module or CORS errors.
- [ ] A real account can register or sign in successfully.
- [ ] The catalog loads data from the backend.
- [ ] Adding an item updates the cart.
- [ ] Removing an item updates the cart and total.
- [ ] Checkout creates an order and handles stock correctly.
- [ ] The completion page retrieves and displays the invoice.
- [ ] An administrator can manage products and view orders.
- [ ] Refund behavior is checked against the backend response.
- [ ] Product images are checked against the current API product list.
- [ ] Backend authorization protects administrative and customer operations.

---

## Notes

- Without a session, public pages such as the home page, sign-in, and registration should remain accessible. Protected pages should show the appropriate sign-in or access-restricted message.
- Clearing frontend `localStorage` removes local session values and may reset demo data; it does not delete records from the backend database.
- Product stock and purchase outcomes are managed by the backend. The frontend displays returned values and validation feedback.
- Keep this README synchronized with the actual API contracts and the frontend code as the project evolves.

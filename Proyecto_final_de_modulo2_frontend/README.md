# Vale's Pet Store — Frontend (Proyecto_final_de_modulo2_frontend)

Vale's Pet Store is the web interface of the PetStore App. A customer can sign up, browse the catalog, build a cart, check out and view a receipt; an administrator can manage inventory, review sales and refund orders.

It is built with **HTML5, CSS3 and JavaScript (ES modules)**: no framework, no `npm` and no build step. Any folder served by a static HTTP server is a working application.

> ⚠️ The project ships in **demo mode** (`USE_MOCK_DATA = true` in `js/config.js`): no API is called and everything is simulated in the browser. See [Connecting to the backend](#connecting-to-the-backend) to switch it off.

---

## Prerequisites

- A modern browser (Chrome, Edge, Firefox, Safari): the app uses ES modules, `fetch` and `localStorage`.
- A static HTTP server. Either of these works:
  - [Python 3](https://www.python.org/downloads/) (`python -m http.server`)
  - The [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) VS Code extension
- Internet access for Google Fonts (Baloo 2 and Nunito Sans). Without it the app still works, using the system font.

> Do not open the `.html` files by double-clicking them (`file://`). Browsers block ES modules over `file://`, and the pages will load without data and without clear errors.

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/Valeria-Jimenez27/DUAD.git
cd DUAD/Proyecto_final_de_modulo2_frontend
```

**2. Install dependencies**

There is nothing to install. The project has no `package.json`.

---

## Configuration

All configuration lives in `js/config.js`:

| Constant | Default | Purpose |
|---|---|---|
| `USE_MOCK_DATA` | `true` | `true` = demo mode (data simulated in the browser). `false` = every page calls the real API. |
| `API_BASE_URL` | `"http://127.0.0.1:5000"` | Base URL used when `USE_MOCK_DATA` is `false`. |

There are no `.env` files or secrets in the frontend: everything in this folder is public by definition.

---

## Usage

**Start the app**

```bash
# from the project folder
python -m http.server 8080
```

Open `http://localhost:8080`.

**Demo accounts** (demo mode does not validate passwords):

| Email | Role |
|---|---|
| `admin@valespetstore.com` | `admin` (with any password) |
| any other email with a valid format | `user` |

**How demo mode behaves**

- The 8 initial products and the cart are stored in `localStorage`, so they survive reloads.
- Every simulated call waits ~350 ms so that loading states are visible.
- Simulated orders and invoices live only in memory and are lost when you change page (see [Known limitations](#known-limitations)).
- To reset the demo: DevTools → *Application* → *Local Storage* → delete the app's keys, or run `localStorage.clear()` in the console.

**Typical customer flow**

1. `register.html` → creates the account and signs in.
2. `catalog.html` → search, filter by category or availability, add products (`product.html` shows the detail).
3. `cart.html` → review or remove products.
4. `order-summary.html` → billing address and payment method (card, SINPE Móvil or cash).
5. `purchase-complete.html` → receipt.

**Typical admin flow**

Sign in → `admin-panel.html` → *Inventario* tab (create, edit, delete products) and *Ventas* tab (view orders, refund).

---

## Project Structure

```
Proyecto_final_de_modulo2_frontend/
│
├── index.html                # Home: hero, categories, contact
├── login.html                # Sign in
├── register.html             # Customer sign-up
├── catalog.html              # Catalog with search and filters
├── product.html              # Product detail (?id=)
├── cart.html                 # Cart
├── order-summary.html        # Billing address + payment method
├── purchase-complete.html    # Receipt (?order_id=)
├── admin-panel.html          # Inventory and sales (admin only)
├── edit-product.html         # Create / edit product (?id= to edit)
│
├── css/
│   ├── variables.css         # Design tokens: colors, typography, spacing
│   ├── base.css              # Reset and global styles
│   ├── layout.css            # Header, containers, grids
│   └── components.css        # Buttons, cards, forms, tables, alerts
│
├── js/
│   ├── config.js             # USE_MOCK_DATA, API_BASE_URL, apiFetch(), ApiError
│   ├── storage.js            # Only access point to localStorage (session, cart)
│   ├── authService.js        # register(), login()
│   ├── productService.js     # getProducts(), getProductById(), getBrands(), getCategories()
│   ├── orderService.js       # cart, checkout, invoice
│   ├── adminService.js       # create/edit/delete product, orders, refunds
│   ├── mockData.js           # Simulated data source for demo mode
│   ├── validators.js         # Regex validations (pure functions)
│   ├── ui.js                 # Alerts, field errors, loading state, access-restricted screen
│   ├── productImage.js       # Resolves each product's image
│   ├── header.js             # Shared header: session, cart counter, search
│   └── <page>.js             # One script per page: index, login, register, catalog,
│                             #   product, cart, orderSummary, purchaseComplete,
│                             #   adminPanel, editProduct
│
└── img/products/             # Logo, hero and product photos
```

Every HTML page loads the same four stylesheets (in the order above), `js/header.js`, and its own page script, all with `type="module"`.

---

## Pages

| Page | Access | Script | Services it uses |
|---|---|---|---|
| `index.html` | Public | `index.js` | `getProducts` (builds the category grid) |
| `login.html` | Public (redirects if already signed in) | `login.js` | `login` |
| `register.html` | Public (redirects if already signed in) | `register.js` | `register`, `login` |
| `catalog.html` | Signed in | `catalog.js` | `getProducts`, `addItemToCart` |
| `product.html` | Signed in | `product.js` | `getProductById`, `addItemToCart` |
| `cart.html` | Signed in | `cart.js` | `getCart`, `removeItemFromCart` |
| `order-summary.html` | Signed in | `orderSummary.js` | `getCart`, `checkout` |
| `purchase-complete.html` | Signed in | `purchaseComplete.js` | `getInvoice` |
| `admin-panel.html` | Admin | `adminPanel.js` | `getProducts`, `deleteProduct`, `getOrders`, `refundOrder` |
| `edit-product.html` | Admin | `editProduct.js` | `getProductById`, `getBrands`, `getCategories`, `createProduct`, `updateProduct` |

State that matters between pages travels in the URL (`?id=`, `?order_id=`, `?search=`, `?category=`) or in `localStorage` (session and cart id).

---

## Architecture

Every page follows the same path, and only in this direction:

```
page.html ──► js/<page>.js ──► js/*Service.js ──► apiFetch() ──► API
 (structure)   (DOM, events)    (which endpoint)    (how)     └─► mockData.js (if USE_MOCK_DATA)
```

- Page scripts **never** call `fetch`: they call services and display `error.message`.
- Services are the only files that know the endpoint paths and the `USE_MOCK_DATA` switch. Each function returns the same shape in both modes.
- `apiFetch()` is the single place that builds headers, adds the token, parses JSON and translates errors.
- `storage.js` is the only file that touches `localStorage` for the session and cart id.
- `validators.js` and `ui.js` hold what forms share: validation rules and the helpers that show alerts, field errors and loading state.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Semantic HTML5 | One page per screen, `lang="es"`, `aria-*` on navigation and icons |
| CSS3 | Custom properties, Flexbox/Grid, `rem`, no framework |
| JavaScript (ES modules) | Per-page logic, no libraries or bundler |
| Fetch API | Network calls, centralized in `apiFetch()` |
| localStorage | Session (token, role), cart id and demo-mode data |
| Google Fonts | Baloo 2 (headings) and Nunito Sans (body text) |

---

## Authentication (client side)

The frontend does not create or verify tokens; it stores and sends them:

1. After a successful login, `login()` saves the `token`, `role` and `customer_id` in `localStorage`.
2. `apiFetch()` adds `Authorization: Bearer <token>` to every request, except those marked `requiresAuth: false`.
3. Each protected page checks `isLoggedIn()` / `isAdmin()` on load. If the check fails it hides the content and shows the "Debes iniciar sesión" ("You must sign in") or "No tienes permisos de administrador" ("You don't have admin permissions") screen (`renderAccessRestricted()` in `ui.js`).
4. "Cerrar sesión" (sign out) clears every app key and returns to `index.html`.

`localStorage` keys: `petstore_token`, `petstore_role`, `petstore_user_name`, `petstore_customer_id`, `petstore_cart_id` (real session) and `petstore_mock_cart_items`, `valespetstore_mock_products_v2` (demo only).

These guards are a usability feature, not security: the role lives in `localStorage` and can be edited in the browser. Anything that must be protected has to be enforced by the API.

---

## Connecting to the backend

The frontend talks to a REST API (the `Proyecto_final_de_modulo2` project). This is the only section that depends on it.

### Switching from demo mode to the real API

1. **Run the API** following its own README (default address `http://127.0.0.1:5000`).
2. **Allow the frontend's origin (CORS) on the API.** The frontend is served from another origin (e.g. `localhost:8080`) and sends an `Authorization` header plus JSON, so the browser sends a preflight `OPTIONS` request first. The API does not currently configure CORS, so every call is blocked until it does. With Flask:

   ```bash
   pip install flask-cors     # and add it to the API's requirements.txt
   ```

   ```python
   from flask_cors import CORS

   app = Flask(__name__)
   CORS(app, origins=["http://localhost:8080", "http://127.0.0.1:8080"])
   ```

   The allowed origin must match exactly how you serve the frontend, port included.
3. **Turn demo mode off** in `js/config.js`:

   ```js
   export const USE_MOCK_DATA = false;
   ```

   Change `API_BASE_URL` if the API runs elsewhere.
4. Serve the frontend (`python -m http.server 8080`) and sign in with an account that exists in the API.

### Endpoints the frontend calls

| Frontend function | Request | Auth | Used in |
|---|---|---|---|
| `register()` | `POST /register`, then `POST /customers` | Public | `register.html` |
| `login()` | `POST /login` | Public | `login.html`, `register.html` |
| `getProducts()` | `GET /products` | User | home, catalog, admin panel |
| `getProductById()` | `GET /products/{id}` | User | detail, edit product |
| `getBrands()` / `getCategories()` | `GET /brands`, `GET /categories` | Public | product form |
| `getOrCreateCart()` | `POST /carts` `{customer_id}` | User | first "add to cart" |
| `getCart()` | `GET /carts/{cart_id}` | User | cart, order summary |
| `addItemToCart()` | `POST /carts/{cart_id}/items` `{product_id, quantity}` | User | catalog, detail |
| `removeItemFromCart()` | `DELETE /carts/{cart_id}/items/{item_id}` | User | cart |
| `checkout()` | `POST /carts/{cart_id}/checkout` `{billing_address, payment_method}` | User | order summary |
| `getInvoice()` | `GET /orders/{id}/invoice` (reads the `invoice` key) | User | receipt |
| `createProduct()` | `POST /products` | Admin | `edit-product.html` |
| `updateProduct()` | `PUT /products/{id}` | Admin | `edit-product.html` |
| `deleteProduct()` | `DELETE /products/{id}` | Admin | admin panel |
| `getOrders()` | `GET /orders` | Admin | admin panel (sales) |
| `refundOrder()` | `POST /orders/{id}/refund` | Admin | admin panel (sales) |

### Data the UI expects

If the API renames any of these fields, update the pages that read them (and `mockData.js`, which mimics them):

| Resource | Fields the frontend reads |
|---|---|
| Product | `product_id`, `name`, `price`, `quantity`, `brand` (name), `category` (name) |
| Brand / category | `brand_id`, `brand_name` / `category_id`, `category_name` |
| Cart | `items[]` with `cart_item_id`, `product_id`, `product_name`, `unit_price`, `quantity`, `subtotal`; and `total` |
| Checkout result | `order_id` |
| Invoice | `order_id`, `order_date`, `items[]`, `total_amount`, `billing_address`, `payment_method` |
| Order (admin) | `order_id`, `customer_id`, `order_date`, `total_amount`, `status` (`completed`, `refunded`, `pending`) |
| Login result | `token`, `role`, `customer_id` |
| Errors | `{ "error": "message" }`, shown to the user as-is |

The payment form sends `tarjeta`, `sinpe` or `efectivo` as `payment_method`.

### Errors

`apiFetch()` throws an `ApiError` (`message`, `status`):

- No response → `"No se pudo conectar con el servidor. Intenta de nuevo."` ("Could not connect to the server. Try again."), `status 0`.
- Non-success response → the `error` text from the API, or a generic message if there is none.

Each page catches it and shows it in its own alert container.

### Things that behave differently against the real API

- **Registration is two requests.** The API keeps the login account and the customer profile separate and links them by email, so `register()` sends the same email in both calls. If the second call fails, the account exists but cannot add products to a cart.
- **Product images.** The API has no image field: the frontend sends `image` when saving a product, but it is not stored. Images are resolved in `productImage.js` (see below).
- **Brand and category arrive as names**, not ids, so `edit-product.html` matches them by name to preselect the dropdowns.
- **Token lifetime is 2 hours.** The frontend does not redirect on an expired token; the user sees the error message and must sign in again.

---

## Technical decisions and rationale

**1. Plain HTML, CSS and JavaScript: no framework, no bundler.**
The scope is a small store and the goal is to master web fundamentals. With no build step, anyone can clone and run it in a minute and there are no dependencies to maintain. *Cost:* more manual DOM code and no reusable components (the header markup is repeated in each HTML file). If the project grows, the service layer can be reused as-is in React or Vue.

**2. Multi-page application: one HTML + one JS file per screen.**
Each screen is independent and easy to locate, and URL parameters make pages reloadable and shareable. *Cost:* every navigation is a full reload, which is why session and cart ids live in `localStorage`.

**3. ES modules (`type="module"`).**
Explicit imports, no globals, one responsibility per file. *Cost:* an HTTP server is required even in development.

**4. Service layer + a single `apiFetch()`.**
Base URL, headers, token and error translation live in one place, so changing the API touches `config.js` and the services, not the ten pages.

**5. Demo mode through a flag, not a fake server.**
`USE_MOCK_DATA` lets the whole app run with nothing else installed, without adding tools such as json-server or MSW. Simulated responses use the same field names as the real ones, so pages cannot tell the modes apart. *Cost:* the mock can drift from the API and must be updated with it; and the flag is edited by hand, so **turn it off for production.**

**6. Token in `localStorage`.**
The API expects a Bearer token in a header, and `localStorage` is the simplest way to keep it across pages. *Cost:* an XSS could read it. An `httpOnly` cookie would be safer but needs changes on the API side. The risk was accepted for the project's scope (see limitation 7).

**7. Access checks in the client are UX only.**
They avoid showing screens a user cannot use; they do not protect anything (see [Authentication](#authentication-client-side)).

**8. Regex form validation in `validators.js`.**
Pure functions (value → message or `null`), reused by every form and independent of the DOM, for immediate feedback. Password rule: at least 8 characters with a letter and a number. This rule exists only in the frontend.

**9. Catalog filtering in the browser.**
The product list is downloaded once and filtered in memory (text, category, available only), normalizing accents and case. Simple and fast for a small catalog. *Cost:* it does not scale to thousands of products; then paginate and filter on the server.

**10. Product images resolved on the client (`productImage.js`).**
Order of precedence: the product's own `image` / `imageUrl`, then a map by product id (1 to 8), then a default image. It is a stopgap until images are stored by the API.

**11. CSS in four layers with variables.**
`variables.css` → `base.css` → `layout.css` → `components.css`, in cascade order. Colors, typography and spacing are design tokens (pastel palette, lilac accent), so a rebrand is a one-file change. It uses `rem`, breakpoints at `48rem` and `30rem`, and honors `prefers-reduced-motion`.

**12. Explicit states on every screen.**
Each page defines loading, empty, no-results and error states, and disables buttons during a request (`setLoading`) to prevent double submits.

**13. Spanish UI (es-CR), English code.**
The audience is Costa Rican (`es-CR` dates, SINPE Móvil). Identifiers are in English and comments in Spanish.

---

## Known limitations

Ordered by impact.

1. **Receipt in demo mode.** `mockInvoices` and `mockOrders` (`js/mockData.js`) are in-memory variables. Going from `order-summary.html` to `purchase-complete.html` reloads the page and they are lost, so the receipt shows "Factura no encontrada." ("Invoice not found."). In the demo's *Sales* tab only the initial order persists and refunds are not kept. Fix: store them in `localStorage`, as products already are.
2. **Cart counter with the real API.** `header.js` counts items with `getLocalCartItems()`, which only demo mode fills, so the counter stays at 0 in real mode. Fix: after adding or removing items, call `getCart()` and emit the `cart-updated` event with the count.
3. **Broken images for ids above 8.** The image map covers ids 1 to 8, and the default image (`img/products/img-1.jpg`) does not exist in the repository. Any other product renders a broken image.
4. **Home page for signed-out visitors in real mode.** `index.js` builds the categories from `GET /products`, which requires a token, so a visitor without a session sees "No fue posible cargar las categorías." ("Could not load categories."). Fix: use `getCategories()`, which is public.
5. **Visible name.** The header shows the email ("Usuario: email@…") because the login response has no name.
6. **Category icons.** `index.js` matches icons by exact name (`alimento`, `farmacia`…), but the actual category names are longer ("Alimento para Perros"), so every category gets the default icon (🐾).
7. **Unescaped HTML.** `catalog.js`, `cart.js`, `adminPanel.js`, `orderSummary.js` and `purchaseComplete.js` build markup with `innerHTML` using values exactly as received. With real data, a product name containing HTML would execute, and the token in `localStorage` would be exposed. Only `index.js` has an `escapeHtml()`; move it to `ui.js` and use it everywhere (or use `textContent`).
8. **Demo data differs from real data.** The demo has 8 products with Spanish category names; the real catalog may have more products with different names.

---

## How to extend the project

**Add a new API call**

1. Create the function in the appropriate service, with its `if (USE_MOCK_DATA)` branch.
2. Add the simulated version in `mockData.js`, with the same fields the API would return.
3. Call it from the page script; do not use `fetch` directly.

**Add a new page**

1. Copy an existing page and keep the four `<link>` stylesheets in order.
2. Load `js/header.js` and the page's own script with `type="module"`.
3. If the page is private, repeat the access block (`isLoggedIn()` / `isAdmin()` + `renderAccessRestricted()`).

**Add or change a form**

Reuse `validateField()` from `validators.js` and the helpers in `ui.js` (`setFieldError`, `showAlert`, `setLoading`). Add new rules to `validators.js`, not inside the page script.

**Before deploying**

- [ ] `USE_MOCK_DATA = false` and `API_BASE_URL` pointing to the real API (HTTPS).
- [ ] The API's CORS restricted to the frontend's real domain.
- [ ] Dynamic HTML escaped (limitation 7).
- [ ] Cart counter and images fixed (limitations 2 and 3).

---

## Troubleshooting

| Symptom | Likely cause | What to do |
|---|---|---|
| Page with no data, module errors in the console | HTML opened via `file://` | Serve the folder with an HTTP server |
| Console: `blocked by CORS policy` | The API does not allow this origin | See step 2 of [Switching from demo mode to the real API](#switching-from-demo-mode-to-the-real-api); the origin must include the port |
| "No se pudo conectar con el servidor" | API not running or `API_BASE_URL` is wrong | Check that the API answers at the configured URL |
| "Tu cuenta no tiene un perfil de cliente asociado" ("Your account has no associated customer profile") | The login response has no `customer_id` | The account needs a customer profile with the same email |
| "Invalid token" or "Token missing" | Token expired (2 h) or session cleared | Sign out and sign in again |
| Demo shows odd or outdated data | `localStorage` holds data from an older version | `localStorage.clear()` and reload |
| Product with a broken image | Product id outside 1 to 8 | See limitation 3 |

---

## Notes

- Without a session only the home page, sign-in and sign-up are reachable; the catalog, product detail, cart and checkout redirect to a "sign in" screen.
- `localStorage` keys start with `petstore_` or `valespetstore_`; deleting them resets the app without affecting other sites.
- Stock is managed by the API (decremented on checkout, restored on refund). The frontend only reflects it visually ("Sin stock" button, maximum quantity).
- Keep this README and `js/mockData.js` in sync with the API whenever its responses change.
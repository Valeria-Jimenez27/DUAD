
# PetStore App(Proyecto_final_de_modulo2)

PetStore App is a backend project designed to demonstrate how to build an e-commerce application from scratch. It originates from a real case where the store was managed only with Excel sheets. The goal is to migrate all data into a relational database and provide a stable and scalable application that supports product management, user and customer creation, sales, and more.

The project strictly follows CRUD principles across all modules — Users, Customers, Products, and Sales — ensuring consistency, clarity, and simplicity for end users. 

# PetStore API

A backend REST API for a pet store e-commerce application, built from a real case where the business was managed entirely with Excel sheets. The goal was to migrate all data into a relational database and provide a stable, scalable backend that supports product management, user authentication, customer records, and sales.

Built as the final project for Module 2 of the DUAD backend development course.

---

## Prerequisites

Before running this project, make sure you have the following installed:

- [Python 3.10+](https://www.python.org/downloads/)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Redis](https://redis.io/) (or a cloud instance via [Redis Cloud](https://redis.com/try-free/))
- [OpenSSL](https://slproweb.com/products/Win32OpenSSL.html) (for RSA key generation)
- [Postman](https://www.postman.com/) (optional, for testing endpoints)

---

## Installation

**1. Clone the repository**

```bash
git clone https://github.com/Valeria-Jimenez27/DUAD.git
cd DUAD/Proyecto_final_de_modulo2
```

**2. Create and activate a virtual environment**

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

**3. Install dependencies**

```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Copy the example file and fill in your values:

```bash
cp .env.example .env
```

Required variables:

```
DB_URI=postgresql://user:password@localhost:5432/petstore
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=your-redis-password
ADMIN_EMAIL=your-admin-email@example.com
ADMIN_PASSWORD=your-secure-password
ADMIN_NAME=Admin
```

**5. Generate RSA keys**

The API uses RS256 JWT authentication. Run these commands from the project root:

```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

This creates `private.pem` (signs tokens) and `public.pem` (verifies them). Both are excluded from version control via `.gitignore`.

---

## Usage

**Seed the initial admin user (run once)**

```bash
python seed.py
```

**Start the API server**

```bash
python run_pet_store.py
```

The server runs at `http://127.0.0.1:5000` by default.

**Run unit tests**

```bash
python run_test_api.py
```

**Typical flow in Postman:**

1. `POST /register` → create a user account
2. `POST /login` → receive a JWT token
3. Use the token in the `Authorization: Bearer <token>` header for all protected endpoints

---

## Project Structure

```
Proyecto_final_de_modulo2/
│
├── app/
│   ├── __init__.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── engine.py          # DB connection and session config
│   ├── models/
│   │   ├── __init__.py
│   │   └── DB.py              # SQLAlchemy table definitions and relationships
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py            # JWT authentication and decorators
│   │   └── Cache.py           # Redis cache manager
│   └── routes/
│       ├── __init__.py
│       ├── users.py           # User endpoints
│       ├── products.py        # Product, brand, and category endpoints
│       ├── customers.py       # Customer endpoints
│       └── sales.py           # Cart, checkout, orders, and refunds
│── pictures/
│       ├── carts_testing.PNG      #example of how to run an endpoint in Postman
│       ├── get_customers.PNG      #example of how to run an endpoint in Postman 
│       ├── post_customers.PNG     #example of how to run an endpoint in Postman           
│       └── put_product.PNG        #example of how to run an endpoint in Postman
├── tests/
│   └── test_api.py            # Unit tests (pytest + unittest.mock)
│
├── private.pem                # RSA private key — excluded via .gitignore
├── public.pem                 # RSA public key — excluded via .gitignore
├── run_pet_store.py           # App entry point
├── run_test_api.py            # Test runner with formatted report
├── seed.py                    # Seeds initial admin user
├── data_tables_testing.py     # Seeds brands, categories, and products
├── requirements.txt           # Project dependencies
├── .env                       # Environment variables — excluded via .gitignore
└── .env.example               # Environment variable template
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python + Flask | Web framework and routing |
| SQLAlchemy | ORM and database management |
| PostgreSQL | Relational database |
| Redis | Caching layer |
| PyJWT + RS256 | JWT authentication with RSA keys |
| bcrypt | Password hashing |
| pytest + unittest.mock | Unit testing |
| python-dotenv | Environment variable management |

---

## Authentication

The API uses JWT tokens signed with RSA keys (RS256 algorithm):

- `POST /register` → creates a user with `role: user`
- `POST /login` → returns a signed JWT
- Protected endpoints require `Authorization: Bearer <token>` header
- Admin-only endpoints additionally require `role: admin`
- To promote a user to admin: `PUT /users/{id}/role` with `{ "role": "admin" }` (admin token required)

---

## Endpoints

**Users**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /register | Public | Create a new user |
| POST | /login | Public | Authenticate and receive JWT |
| GET | /users | Admin | List all users |
| GET | /users/{id} | Admin | Get user by ID |
| PUT | /users/{id} | Admin | Update user info |
| PUT | /users/{id}/role | Admin | Promote or demote user role |
| DELETE | /users/{id} | Admin | Delete user |

**Customers**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /customers | Public | Create a new customer |
| GET | /customers | Admin | List all customers |
| GET | /customers/{id} | Admin | Get customer by ID |
| PUT | /customers/{id} | Admin | Update customer |
| DELETE | /customers/{id} | Admin | Delete customer |

**Products**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | /products | User | List all products |
| GET | /products/{id} | User | Get product by ID |
| POST | /products | Admin | Create product |
| PUT | /products/{id} | Admin | Update product |
| DELETE | /products/{id} | Admin | Delete product |
| GET | /brands | Public | List all brands |
| GET | /categories | Public | List all categories |

**Sales**

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | /carts | User | Create shopping cart |
| GET | /carts/{cart_id} | User | View cart details |
| POST | /carts/{cart_id}/items | User | Add item to cart |
| DELETE | /carts/{cart_id}/items/{item_id} | User | Remove item from cart |
| POST | /carts/{cart_id}/checkout | User | Checkout and create order |
| GET | /orders | Admin | List all orders |
| GET | /orders/{id}/invoice | User | Retrieve invoice |
| POST | /orders/{id}/refund | Admin | Refund order |

---

## Entity-Relationship Diagram

```
users ──────────────────────── customers
 id (PK)                        customer_id (PK)
 name                           first_name
 email                          last_name
 password                       email
 role                           phone
                                address
                                user_id (FK → users.id)

customers ──────────────── shopping_carts ──────────── cart_items
 customer_id (PK)               cart_id (PK)            cart_item_id (PK)
                                customer_id (FK)         cart_id (FK)
                                created_at               product_id (FK)
                                is_active                quantity

customers ──────────────── orders ──────────────────── order_details
 customer_id (PK)               order_id (PK)           order_detail_id (PK)
                                customer_id (FK)         order_id (FK)
                                order_date               product_id (FK)
                                total_amount             quantity
                                billing_address          unit_price
                                payment_method
                                status

products ──────────── brands          products ──────────── categories
 product_id (PK)       brand_id (PK)   product_id (PK)       category_id (PK)
 brand_id (FK)         brand_name      category_id (FK)       category_name
 category_id (FK)
 name
 price
 quantity
```

---

## Examples in Postman

![Delete products](docs/delete_products.png)

![Get Customers](docs/get_customers.png)

![Post Customers](docs/post_customers_example.png)

![Put products](docs/put_product.png)

![Carts testing](docs/carts_testing.png)

---

## Notes

- Customers must be created before carts can be assigned to them.
- Product stock is automatically decremented on checkout and restored on refund.
- Redis cache is invalidated automatically when products, orders, or invoices are modified.
- Sensitive files (`.env`, `private.pem`, `public.pem`) must never be committed — all are covered by `.gitignore`.
- Run `seed.py` only once per environment to avoid duplicate admin errors.

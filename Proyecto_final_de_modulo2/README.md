
# PetStore App(Proyecto_final_de_modulo2)

PetStore App is a backend project designed to demonstrate how to build an e-commerce application from scratch. It originates from a real case where the store was managed only with Excel sheets. The goal is to migrate all data into a relational database and provide a stable and scalable application that supports product management, user and customer creation, sales, and more.

The project strictly follows CRUD principles across all modules — Users, Customers, Products, and Sales — ensuring consistency, clarity, and simplicity for end users. 


## Installation

**Clone the repository**

git clone https://github.com/Valeria-Jimenez27/DUAD/tree/Proyecto_final_de_modulo2/Proyecto_final_de_modulo2

cd Proyecto_final_de_modulo2

**Create virtual environment**

python -m venv venv

.\venv\Scripts\Activate.ps1    # Windows

**Install dependencies**
pip install -r requirements.txt

**Set up environment variables**

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
```

## Tech tools

Python

Flask

SQLAlchemy

PostgreSQL

Redis

Postman

JWT Authentication with RSA keys

.env for environment variables (excluded via .gitignore)

Readme.so

Dependencies are listed in requirements.txt.


## RSA Key Generation

The app uses RS256 JWT authentication. You must generate the RSA key pair before running the server. Without these files, the server will fail on any authenticated request.

Run these commands in the project root:

```bash
openssl genrsa -out private.pem 2048
openssl rsa -in private.pem -pubout -out public.pem
```

This will create `private.pem` (used to sign tokens) and `public.pem` (used to verify them). Both files are excluded from version control via `.gitignore`.

# Entity-Relationship Diagram

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

products ──────────── brands
 product_id (PK)        brand_id (PK)
 brand_id (FK)          brand_name
 category_id (FK)
 name               products ──────────── categories
 price               product_id (PK)       category_id (PK)
 quantity            category_id (FK)      category_name
```


## Deployment

To deploy this project run:

**Start the API server:**

python run_pet_store.py

**Run unit tests:**

python run_test_api.py


## Authentication


The API uses JWT signed with RSA keys:

Algorithm: RS256 (RSA Signature with SHA-256).

Password hashing: bcrypt for secure storage and verification.

private.pem → used to sign tokens.

public.pem → used to verify tokens.

Keys are stored securely in .env and excluded from version control.

Flow: Register → Login → Receive JWT → Access protected endpoints.
## Code Structure


The application is structured into four main modules:

products.py → handles product creation, updates, stock management, and deletion.

users.py → manages user registration, login, CRUD, and secure authentication.

customers.py → manages customer records and their relationship with carts and orders.

sales.py → handles shopping carts, checkout, orders, invoices, and refunds.

Additional supporting modules include:

engine.py → connects to DB.py, where all tables, relationships, and store data are defined.

auth.py → provides secure user authentication using JWT tokens with RS256 and password hashing via bcrypt.

Cache.py → integrates Redis for caching invoices, orders, and product data.

Unit testing scripts → written with pytest, along with a runner module to execute them automatically(run_test_api.py).

Main runner module → executes the core application logic (run_pet_store.py).

Proyecto_final_de_modulo2/
├── requirements.txt         # Project dependencies 
├── run_pet_store.py         # Main runner
├── env_example.py           # Example configuration of the REDIS and Postgress credentials
├── DB.py                    # Data Base
├── engine.py                # Data base configuration 
├── users.py                 # Users module and endpoints
├── products.py              # Products module and endpoints
├── customers.py             # Customers module and endpoints
├── sales.py                 # Sales module and endpoints
├── Cache.py                 # Cache module using Redis
├── auth.py                  # Authentication using JWT tokens
│   ├── private.pem          # Private Key hide with .gitignore
│   ├── public.pem.          # Public Key hide with .gitignore
└── run_test_api             # Run unit tests
    ├── test.api.py          # Unit testing

## Endpoints

**Users**

POST /register → Create a new user.

POST /login → Authenticate and receive JWT.

GET /users → List all users (admin only).

PUT /users/{id} → Update user.

DELETE /users/{id} → Delete user.

**Customers**

POST /customers → Create a new customer.

GET /customers → List all customers.

GET /customers/{id} → Get customer details.

PUT /customers/{id} → Update customer.

DELETE /customers/{id} → Delete customer.

**Products**

POST /products → Create product.

GET /products → List products.

GET /products/{id} → Get product details.

PUT /products/{id} → Update product.

DELETE /products/{id} → Delete product.

**Sales**

POST /carts → Create shopping cart.

POST /carts/{cart_id}/items → Add item to cart.

DELETE /carts/{cart_id}/items/{item_id} → Remove item from cart.

GET /carts/{cart_id} → View cart details.

POST /carts/{cart_id}/checkout → Checkout and create order.

GET /orders → List all orders (admin only).

GET /orders/{id}/invoice → Retrieve invoice.

POST /orders/{id}/refund → Refund order.
## Examples in Postman

![Carts testing](docs/carts_testing.png)

![Get Customers](docs/get_customers.png)

![Post Customers](docs/post_customers_example.png)

![Put products](docs/put_product.png)

![Delete products](docs/delete_products.png)
## Notes

-Customers must be created before carts can be assigned.

-Product stock is automatically updated during checkout and refund.

-Cache invalidation is handled for invoices, orders, and products.

-Sensitive files (.env, private.pem, public.pem) must be excluded from version control using .gitignore.


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

![Carts testing](C:\Users\hp\Pictures\Screenshots\carts_testing)

![Get Customers](C:\Users\hp\Pictures\Screenshots\get_customers)

![Post Customers](C:\Users\hp\Pictures\Screenshots\post_customers_example)

![Put products](C:\Users\hp\Pictures\Screenshots\put_product)

![Delete products](C:\Users\hp\Pictures\Screenshots\delete_products)
## Notes

-Customers must be created before carts can be assigned.

-Product stock is automatically updated during checkout and refund.

-Cache invalidation is handled for invoices, orders, and products.

-Sensitive files (.env, private.pem, public.pem) must be excluded from version control using .gitignore.

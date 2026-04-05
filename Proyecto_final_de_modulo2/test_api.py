import pytest
from unittest.mock import patch, MagicMock
import bcrypt
from run_pet_store import app


@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def mock_user_token():
    #Simula un token válido con rol user
    return {"Authorization": "Bearer faketoken"}

def mock_admin_token():
    #Simula un token válido con rol admin
    return {"Authorization": "Bearer faketoken"}



#testing users
def test_register_success(client):
    # arrange
    with patch("users.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.post("/register", json={
            "name": "Test User",
            "email": "test@test.com",
            "password": "password123"
        })
        # assert
        assert response.status_code == 201
        assert response.get_json()["message"] == "User registered successfully"


def test_register_duplicate_email(client):
    # arrange
    with patch("users.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = MagicMock()
        # act
        response = client.post("/register", json={
            "name": "Test User",
            "email": "existing@test.com",
            "password": "password123"
        })
        # assert
        assert response.status_code == 400
        assert response.get_json()["error"] == "Email already registered"


def test_login_success(client):
    # arrange
    with patch("users.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.role = "user"
        mock_user.password = bcrypt.hashpw(
            "password123".encode(), bcrypt.gensalt()
        ).decode()
        db.query.return_value.filter.return_value.first.return_value = mock_user
        # act
        response = client.post("/login", json={
            "email": "test@test.com",
            "password": "password123"
        })
        # assert
        assert response.status_code == 200
        assert "token" in response.get_json()


def test_login_wrong_password(client):
    # arrange
    with patch("users.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        mock_user = MagicMock()
        mock_user.password = bcrypt.hashpw(
            "password123".encode(), bcrypt.gensalt()
        ).decode()
        db.query.return_value.filter.return_value.first.return_value = mock_user
        # act
        response = client.post("/login", json={
            "email": "test@test.com",
            "password": "wrongpassword"
        })
        # assert
        assert response.status_code == 401
        assert response.get_json()["error"] == "Invalid email or password"


def test_login_nonexistent_user(client):
    # arrange
    with patch("users.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.post("/login", json={
            "email": "noexiste@test.com",
            "password": "password123"
        })
        # assert
        assert response.status_code == 401
        assert response.get_json()["error"] == "Invalid email or password"


def test_get_users_without_token(client):
    # arrange - no hay token
    # act
    response = client.get("/users")
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_get_users_with_user_role(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("users.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "user"}
        db = MagicMock()
        mock_session.return_value = db
        # act
        response = client.get("/users", headers=mock_user_token())
        # assert
        assert response.status_code == 403
        assert response.get_json()["error"] == "Forbidden"


def test_get_users_with_admin_role(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("users.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "admin"}
        db = MagicMock()
        mock_session.return_value = db
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "Admin"
        mock_user.email = "admin@test.com"
        mock_user.role = "admin"
        db.query.return_value.all.return_value = [mock_user]
        # act
        response = client.get("/users", headers=mock_admin_token())
        # assert
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)


#testing customers
def test_create_customer_success(client):
    # arrange
    with patch("customers.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.post("/customers", json={
            "first_name": "Francisco",
            "last_name": "Rojas",
            "email": "fra11@gmail.com",
            "phone": "87654324",
            "address": "Cartago, Guadalupe"
        })
        # assert
        assert response.status_code == 201
        assert response.get_json()["message"] == "Customer information saved successfully"


def test_create_customer_duplicate_email(client):
    # arrange
    with patch("customers.SessionLocal") as mock_session:
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = MagicMock()
        # act
        response = client.post("/customers", json={
            "first_name": "Francisco",
            "last_name": "Rojas",
            "email": "fra11@gmail.com",
            "phone": "87654324",
            "address": "Cartago, Guadalupe"
        })
        # assert
        assert response.status_code == 400
        assert response.get_json()["error"] == "Email already registered"


def test_get_customers_without_token(client):
    # arrange - no hay token
    # act
    response = client.get("/customers")
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_delete_customer_without_token(client):
    # arrange - no hay token
    # act
    response = client.delete("/customers/1")
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_delete_customer_not_found(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("customers.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "admin"}
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.delete("/customers/100",
        headers=mock_admin_token())
        # assert
        assert response.status_code == 404
        assert response.get_json()["error"] == "Customer not found"


#testing products
def test_get_products_from_db(client):
    # arrange
    with patch("products.cache_manager") as mock_cache, \
        patch("products.SessionLocal") as mock_session:
        mock_cache.get_data.return_value = None
        db = MagicMock()
        mock_session.return_value = db
        mock_product = MagicMock()
        mock_product.product_id = 1
        mock_product.name = "Nutrisource Large Breed"
        mock_product.price = 65.00
        mock_product.quantity = 30
        mock_product.brand.brand_name = "NutriSource"
        mock_product.category.category_name = "Dog Food"
        db.query.return_value.all.return_value = [mock_product]
        # act
        response = client.get("/products")
        # assert
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)
        assert response.get_json()[0]["name"] == "Nutrisource Large Breed"


def test_get_products_from_cache(client):
    # arrange
    with patch("products.cache_manager") as mock_cache:
        mock_cache.get_data.return_value = [
            {"product_id": 1, "name": "Cached Product", "price": 65.00}
        ]
        # act
        response = client.get("/products")
        # assert
        assert response.status_code == 200
        assert response.get_json()[0]["name"] == "Cached Product"


def test_get_product_by_id_success(client):
    # arrange
    with patch("products.cache_manager") as mock_cache, \
        patch("products.SessionLocal") as mock_session:
        mock_cache.get_data.return_value = None
        db = MagicMock()
        mock_session.return_value = db
        mock_product = MagicMock()
        mock_product.product_id = 1
        mock_product.name = "Nutrisource Large Breed"
        mock_product.price = 65.00
        mock_product.quantity = 30
        mock_product.brand.brand_name = "NutriSource"
        mock_product.category.category_name = "Dog Food"
        db.query.return_value.filter.return_value.first.return_value = mock_product
        # act
        response = client.get("/products/1")
        # assert
        assert response.status_code == 200
        assert response.get_json()["product_id"] == 1


def test_get_product_not_found(client):
    # arrange
    with patch("products.cache_manager") as mock_cache, \
        patch("products.SessionLocal") as mock_session:
        mock_cache.get_data.return_value = None
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.get("/products/100")
        # assert
        assert response.status_code == 404
        assert response.get_json()["error"] == "Product not found"


def test_create_product_without_token(client):
    # arrange - no hay token
    # act
    response = client.post("/products", json={
        "name": "New Product",
        "price": 50.00,
        "quantity": 10,
        "brand_id": 1,
        "category_id": 1
    })
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_create_product_with_admin(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("products.cache_manager"), \
        patch("products.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "admin"}
        db = MagicMock()
        mock_session.return_value = db
        db.refresh.side_effect = lambda x: setattr(x, "product_id", 1)
        # act
        response = client.post("/products", json={
            "name": "New Product",
            "price": 50.00,
            "quantity": 10,
            "brand_id": 1,
            "category_id": 1
        }, headers=mock_admin_token())
        # assert
        assert response.status_code == 201
        assert response.get_json()["message"] == "Product created successfully"


def test_update_product_without_token(client):
    # arrange - no hay token
    # act
    response = client.put("/products/1", json={"price": 99.00})
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_delete_product_not_found(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("products.cache_manager"), \
        patch("products.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "admin"}
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.delete("/products/999",
        headers=mock_admin_token())
        # assert
        assert response.status_code == 404
        assert response.get_json()["error"] == "Product not found"


def test_get_brands_success(client):
    # arrange
    with patch("products.cache_manager") as mock_cache, \
        patch("products.SessionLocal") as mock_session:
        mock_cache.get_data.return_value = None
        db = MagicMock()
        mock_session.return_value = db
        mock_brand = MagicMock()
        mock_brand.brand_id = 1
        mock_brand.brand_name = "NutriSource"
        db.query.return_value.all.return_value = [mock_brand]
        # act
        response = client.get("/brands")
        # assert
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)


def test_get_categories_success(client):
    # arrange
    with patch("products.cache_manager") as mock_cache, \
        patch("products.SessionLocal") as mock_session:
        mock_cache.get_data.return_value = None
        db = MagicMock()
        mock_session.return_value = db
        mock_category = MagicMock()
        mock_category.category_id = 1
        mock_category.category_name = "Dog Food"
        db.query.return_value.all.return_value = [mock_category]
        # act
        response = client.get("/categories")
        # assert
        assert response.status_code == 200
        assert isinstance(response.get_json(), list)


#testing sales
def test_create_cart_without_token(client):
    # arrange - no hay token
    # act
    response = client.post("/carts", json={"customer_id": 1})
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_create_cart_already_exists(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "user"}
        db = MagicMock()
        mock_session.return_value = db
        mock_cart = MagicMock()
        mock_cart.cart_id = 1
        db.query.return_value.filter.return_value.first.return_value = mock_cart
        # act
        response = client.post("/carts", json={"customer_id": 1},
        headers=mock_user_token())
        # assert
        assert response.status_code == 200
        assert response.get_json()["message"] == "Customer already has an active cart"


def test_get_cart_not_found(client):
    # arrange - mockear jwt.decode para simular token con rol user
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "user"}
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.get("/carts/999", headers=mock_user_token())
        # assert
        assert response.status_code == 404
        assert response.get_json()["error"] == "Cart not found"


def test_add_item_insufficient_stock(client):
    # arrange - mockear jwt.decode para simular token con rol user
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "user"}
        db = MagicMock()
        mock_session.return_value = db
        mock_cart = MagicMock()
        mock_product = MagicMock()
        mock_product.quantity = 2
        db.query.return_value.filter.return_value.first.side_effect = [
            mock_cart, mock_product
        ]
        # act
        response = client.post("/carts/1/items", json={
            "product_id": 1,
            "quantity": 10
        }, headers=mock_user_token())
        # assert
        assert response.status_code == 400
        assert "Insufficient stock" in response.get_json()["error"]


def test_checkout_without_token(client):
    # arrange - no hay token
    # act
    response = client.post("/carts/1/checkout", json={
        "billing_address": "Cartago",
        "payment_method": "credit_card"
    })
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_checkout_missing_billing_address(client):
    # arrange - mockear jwt.decode para simular token con rol user
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "user"}
        db = MagicMock()
        mock_session.return_value = db
        mock_cart = MagicMock()
        mock_cart.items = [MagicMock()]
        db.query.return_value.filter.return_value.first.return_value = mock_cart
        # act
        response = client.post("/carts/1/checkout", json={
            "payment_method": "credit_card"
        }, headers=mock_user_token())
        # assert
        assert response.status_code == 400
        assert response.get_json()["error"] == "Billing address is required"


def test_checkout_missing_payment_method(client):
    # arrange - mockear jwt.decode para simular token con rol user
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "user"}
        db = MagicMock()
        mock_session.return_value = db
        mock_cart = MagicMock()
        mock_cart.items = [MagicMock()]
        db.query.return_value.filter.return_value.first.return_value = mock_cart
        # act
        response = client.post("/carts/1/checkout", json={
            "billing_address": "Cartago"
        }, headers=mock_user_token())
        # assert
        assert response.status_code == 400
        assert response.get_json()["error"] == "Payment method is required"


def test_get_invoice_from_cache(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.cache_manager") as mock_cache:
        mock_decode.return_value = {"id": 1, "role": "user"}
        mock_cache.get_data.return_value = {
            "order_id": 1,
            "total_amount": 110.00
        }
        # act
        response = client.get("/orders/1/invoice", headers=mock_user_token())
        # assert
        assert response.status_code == 200
        assert response.get_json()["invoice"]["order_id"] == 1


def test_get_invoice_not_found(client):
    # arrange - mockear jwt.decode para simular token con rol user
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.cache_manager") as mock_cache, \
        patch("sales.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "user"}
        mock_cache.get_data.return_value = None
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.get("/orders/100/invoice", headers=mock_user_token())
        # assert
        assert response.status_code == 404
        assert response.get_json()["error"] == "Order not found"


def test_refund_without_token(client):
    # arrange - no hay token
    # act
    response = client.post("/orders/1/refund")
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"


def test_refund_order_not_found(client):
    # arrange
    with patch("auth.jwt.decode") as mock_decode, \
        patch("sales.cache_manager"), \
        patch("sales.SessionLocal") as mock_session:
        mock_decode.return_value = {"id": 1, "role": "admin"}
        db = MagicMock()
        mock_session.return_value = db
        db.query.return_value.filter.return_value.first.return_value = None
        # act
        response = client.post("/orders/100/refund", headers=mock_admin_token())
        # assert
        assert response.status_code == 404
        assert response.get_json()["error"] == "Order not found"


def test_get_orders_without_token(client):
    # arrange - no hay token
    # act
    response = client.get("/orders")
    # assert
    assert response.status_code == 401
    assert response.get_json()["error"] == "Token missing"
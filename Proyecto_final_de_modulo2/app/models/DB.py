from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.engine import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="user")

    customer = relationship("Customer", back_populates="user", uselist=False)


class Product(Base):
    __tablename__ = "products"
    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    brand_id = Column(Integer, ForeignKey("brands.brand_id"))
    category_id = Column(Integer, ForeignKey("categories.category_id"))

    brand = relationship("Brand", back_populates="products")
    category = relationship("Category", back_populates="products")


class Brand(Base):
    __tablename__ = "brands"
    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String, nullable=False)

    products = relationship("Product", back_populates="brand")


class Category(Base):
    __tablename__ = "categories"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False)

    products = relationship("Product", back_populates="category")


class Customer(Base):
    __tablename__ = "customers"
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    
    user = relationship("User", back_populates="customer")
    shopping_carts = relationship("ShoppingCart", back_populates="customer")
    orders = relationship("Order", back_populates="customer")


class ShoppingCart(Base):
    __tablename__ = "shopping_carts"
    cart_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    created_at = Column(DateTime, default=datetime.now)
    is_active = Column(Boolean, default=True)

    customer = relationship("Customer", back_populates="shopping_carts")
    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"
    cart_item_id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey("shopping_carts.cart_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)

    cart = relationship("ShoppingCart", back_populates="items")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.customer_id"))
    order_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float, nullable=False)
    billing_address = Column(String, nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, default="completed")

    customer = relationship("Customer", back_populates="orders")
    details = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "order_details"
    order_detail_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)

    order = relationship("Order", back_populates="details")
    product = relationship("Product")
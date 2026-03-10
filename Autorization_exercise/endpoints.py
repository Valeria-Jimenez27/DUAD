from flask import Blueprint, request
from engine import SessionLocal
from DB import User, Product, Bill
from datetime import datetime
from authorization import token_required, admin_required, generate_token

api = Blueprint("api", __name__)


#Registro de nuevos usuarios y admin
@api.route("/register", methods=["POST"])
def register():
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data or "name" not in data or "email" not in data or "password" not in data:
            return {"error": "Missing fields"}, 400
        existing = db.query(User).filter(User.email == data["email"]).first()
        if existing:
            return {"error": "User already exists"}, 400

        role = data.get("role", "user")

        new_user = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            role=role
        )
        db.add(new_user)
        db.commit()

        token = generate_token(new_user)

        return {"message": "User created successfully", "token": token}, 201
    finally:
        db.close()


@api.route("/login", methods=["POST"])
def login():
    db = SessionLocal()
    try:
        data = request.get_json()
        if not data or "email" not in data or "password" not in data:
            return {"error": "Missing fields"}, 400
        user = db.query(User).filter(User.email == data["email"]).first()
        if not user or user.password != data["password"]:
            return {"error": "Invalid credentials"}, 401

        token = generate_token(user)
        return {"token": token}
    finally:
        db.close()


#CRUD PRODUCTOS (SOLO ADMIN)
@api.route("/products", methods=["POST"])
@token_required
@admin_required
def create_product():
    db = SessionLocal()
    data = request.get_json()
    product = Product(
        name=data["name"],
        price=data["price"],
        entry_date=datetime.strptime(data["entry_date"], "%Y-%m-%d").date(),
        quantity=data["quantity"]
    )
    db.add(product)
    db.commit()
    return {"message": "Product created"}, 201



@api.route("/products", methods=["GET"])
@token_required
def get_products():
    db = SessionLocal()
    products = db.query(Product).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "quantity": p.quantity
        })
    return result


@api.route("/buy", methods=["POST"])
@token_required
def buy_product():
    db = SessionLocal()
    data = request.get_json()
    product = db.query(Product).get(data["product_id"])
    if not product:
        return {"error": "Product not found"}, 404
    if product.quantity < data["quantity"]:
        return {"error": "Not enough in stock"}, 400
    total = product.price * data["quantity"]
    bill = Bill(
        user_id=request.user["id"],
        product_id=product.id,
        quantity=data["quantity"],
        total_price=total
    )
    product.quantity -= data["quantity"]

    db.add(bill)
    db.commit()

    return {"message": "Purchase successful"}


@api.route("/my_bills", methods=["GET"])
@token_required
def my_bills():
    db = SessionLocal()
    bills = db.query(Bill).filter(
        Bill.user_id == request.user["id"]
    ).all()
    result = []
    for bill in bills:
        result.append({
            "bill_id": bill.id,
            "product": bill.product.name,
            "quantity": bill.quantity,
            "total": bill.total_price
        })
    return result
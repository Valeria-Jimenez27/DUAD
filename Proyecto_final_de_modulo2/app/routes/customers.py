from flask import Blueprint, request, jsonify
from app.database.engine import SessionLocal
from app.models.DB import Customer
from app.services.auth import token_required, admin_required

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/customers", methods=["GET"])
@token_required
@admin_required
def get_customers():
    db = SessionLocal()
    try:
        customers = db.query(Customer).all()
        result = [
            {
                "customer_id": c.customer_id,
                "first_name": c.first_name,
                "last_name": c.last_name,
                "email": c.email,
                "phone": c.phone,
                "address": c.address
            } for c in customers
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customers_bp.route("/customers/<int:id>", methods=["GET"])
@token_required
@admin_required
def get_customer(id):
    db = SessionLocal()
    try:
        c = db.query(Customer).filter(Customer.customer_id == id).first()
        if not c:
            return jsonify({"error": "Customer not found"}), 404
        return jsonify({
            "customer_id": c.customer_id,
            "first_name": c.first_name,
            "last_name": c.last_name,
            "email": c.email,
            "phone": c.phone,
            "address": c.address
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customers_bp.route("/customers", methods=["POST"])
def create_customer():
    data = request.json
    db = SessionLocal()
    try:
        existing = db.query(Customer).filter(Customer.email == data["email"]).first()
        if existing:
            return jsonify({"error": "Email already registered"}), 400
        customer = Customer(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data.get("phone"),
            address=data.get("address")
        )
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return jsonify({
            "message": "Customer information saved successfully",
            "customer_id": customer.customer_id
        }), 201
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customers_bp.route("/customers/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_customer(id):
    data = request.json
    db = SessionLocal()
    try:
        c = db.query(Customer).filter(Customer.customer_id == id).first()
        if not c:
            return jsonify({"error": "Customer not found"}), 404
        c.first_name = data.get("first_name", c.first_name)
        c.last_name = data.get("last_name", c.last_name)
        c.email = data.get("email", c.email)
        c.phone = data.get("phone", c.phone)
        c.address = data.get("address", c.address)
        db.commit()
        return jsonify({"message": "Customer updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@customers_bp.route("/customers/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_customer(id):
    db = SessionLocal()
    try:
        c = db.query(Customer).filter(Customer.customer_id == id).first()
        if not c:
            return jsonify({"error": "Customer not found"}), 404
        db.delete(c)
        db.commit()
        return jsonify({"message": "Customer deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
from flask import Blueprint, request, jsonify
from app.database.engine import SessionLocal
from app.models.DB import User, Customer
from app.services.auth import token_required, admin_required, generate_token
import bcrypt

users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    db = SessionLocal()

    try:
        # Datos enviados desde el formulario
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data["email"].strip().lower()
        password = data["password"]
        phone = data.get("phone")
        address = data.get("address")

        # Validaciones básicas
        if not first_name or not last_name:
            return jsonify({"error": "First name and last name are required"}), 400

        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400

        # Verificar que el email no exista como usuario
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        # Crear contraseña encriptada
        hashed_password = bcrypt.hashpw(
            password.encode(),
            bcrypt.gensalt()
        ).decode()

        # Crear usuario
        user = User(
            name=f"{first_name} {last_name}",
            email=email,
            password=hashed_password,
            role="user"
        )

        db.add(user)

        # Necesitamos el ID generado del usuario
        db.flush()

        # Crear Customer vinculado directamente con User
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            user_id=user.id
        )

        db.add(customer)

        # Guardar ambos registros en una sola transacción
        db.commit()

        db.refresh(user)
        db.refresh(customer)

        return jsonify({
            "message": "User registered successfully",
            "id": user.id,
            "customer_id": customer.customer_id
        }), 201

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


@users_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    db = SessionLocal()

    try:
        email = data["email"].strip().lower()

        user = db.query(User).filter(User.email == email).first()

        if not user or not bcrypt.checkpw(
            data["password"].encode(),
            user.password.encode()
        ):
            return jsonify({"error": "Invalid email or password"}), 401

        token = generate_token(user)

        # Buscar Customer mediante la relación con User
        customer = db.query(Customer).filter(
            Customer.user_id == user.id
        ).first()

        return jsonify({
            "message": "Login successful",
            "token": token,
            "role": user.role,
            "customer_id": customer.customer_id if customer else None
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


# ---------------------------------------------------------
# Actualizar rol de usuario
# ---------------------------------------------------------

@users_bp.route("/users/<int:id>/role", methods=["PUT"])
@token_required
@admin_required
def update_user_role(id):
    data = request.json
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        user.role = data["role"]

        db.commit()

        return jsonify({
            "message": "User role updated successfully"
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


# ---------------------------------------------------------
# Obtener usuarios
# ---------------------------------------------------------

@users_bp.route("/users", methods=["GET"])
@token_required
@admin_required
def get_users():
    db = SessionLocal()

    try:
        users = db.query(User).all()

        result = []

        for user in users:
            result.append({
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


# ---------------------------------------------------------
# Obtener usuario por ID
# ---------------------------------------------------------

@users_bp.route("/users/<int:id>", methods=["GET"])
@token_required
@admin_required
def get_user(id):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()


# ---------------------------------------------------------
# Eliminar usuario
# ---------------------------------------------------------

@users_bp.route("/users/<int:id>", methods=["DELETE"])
@token_required
@admin_required
def delete_user(id):
    db = SessionLocal()

    try:
        user = db.query(User).filter(User.id == id).first()

        if not user:
            return jsonify({"error": "User not found"}), 404

        db.delete(user)
        db.commit()

        return jsonify({
            "message": "User deleted successfully"
        }), 200

    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        db.close()
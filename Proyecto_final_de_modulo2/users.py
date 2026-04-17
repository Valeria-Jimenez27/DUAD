from flask import Blueprint, request, jsonify
from engine import SessionLocal
from DB import User
from auth import generate_token, token_required, admin_required
import bcrypt

users_bp = Blueprint("users", __name__)


@users_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == data["email"]).first()
        if existing:
            return jsonify({"error": "Email already registered"}), 400
        hashed_password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
        user = User(
            name=data["name"],
            email=data["email"],
            password=hashed_password,
            role="user"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return jsonify({"message": "User registered successfully", "id": user.id}), 201
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
        user = db.query(User).filter(User.email == data["email"]).first()
        if not user or not bcrypt.checkpw(data["password"].encode(), user.password.encode()):
            return jsonify({"error": "Invalid email or password"}), 401
        token = generate_token(user)
        return jsonify({
            "message": "Login successful",
            "token": token,
            "role": user.role
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@users_bp.route("/users", methods=["GET"])
@token_required
@admin_required
def get__all_users():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        result = [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@users_bp.route("/users/<int:id>", methods=["GET"])
@token_required
@admin_required
def get_user(id):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        return jsonify({"id": user.id, "name": user.name, "email": user.email, "role": user.role}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


@users_bp.route("/users/<int:id>", methods=["PUT"])
@token_required
@admin_required
def update_user(id):
    data = request.json
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            return jsonify({"error": "User not found"}), 404
        user.name = data.get("name", user.name)
        user.email = data.get("email", user.email)
        user.role = data.get("role", user.role)
        if "password" in data:
            user.password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt()).decode()
        db.commit()
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()


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
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()
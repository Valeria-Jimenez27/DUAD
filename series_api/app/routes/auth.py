import os
from flask import request, jsonify
from app.routes import api_bp
from app.auth import create_token


@api_bp.route("/auth/login", methods=["POST"])
def login():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    username = body.get("username", "")
    password = body.get("password", "")

    if not username or not password:
        return jsonify({"error": "'username' y 'password' son requeridos"}), 400

    expected_user = os.environ.get("ADMIN_USERNAME", "")
    expected_pass = os.environ.get("ADMIN_PASSWORD", "")

    if not expected_user or not expected_pass:
        return jsonify({"error": "Credenciales de admin no configuradas en el servidor"}), 503

    if username != expected_user or password != expected_pass:
        return jsonify({"error": "Credenciales incorrectas"}), 401

    try:
        token = create_token(username)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503

    return jsonify({"token": token, "expires_in": 86400}), 200

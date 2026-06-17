import os
from datetime import datetime, timezone, timedelta
from functools import wraps

import jwt
from flask import request, jsonify, g


def _secret() -> str:
    key = os.environ.get("JWT_SECRET_KEY", "")
    if not key:
        raise RuntimeError("JWT_SECRET_KEY no está configurado en el .env")
    return key


def create_token(username: str) -> str:
    payload = {
        "sub": username,
        "exp": datetime.now(tz=timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, _secret(), algorithm="HS256")


def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Se requiere token. Incluí 'Authorization: Bearer <token>'"}), 401
        token = auth_header[7:]
        try:
            payload = jwt.decode(token, _secret(), algorithms=["HS256"])
            g.user = payload.get("sub")
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expirado. Volvé a hacer login"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token inválido"}), 401
        return f(*args, **kwargs)
    return decorated

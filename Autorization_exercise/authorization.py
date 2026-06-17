import jwt
from flask import request
from functools import wraps
import os

BASE_DIR = os.path.dirname(__file__)
PRIVATE_KEY_PATH = os.path.join(BASE_DIR, "private.pem")
PUBLIC_KEY_PATH = os.path.join(BASE_DIR, "public.pem")

with open(PRIVATE_KEY_PATH, "rb") as f:
    PRIVATE_KEY = f.read()

with open(PUBLIC_KEY_PATH, "rb") as f:
    PUBLIC_KEY = f.read()


def generate_token(user):
    payload = {
        "id": user.id,
        "role": user.role
    }
    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256")
    return token


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return {"error": "Token missing"}, 401
        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, PUBLIC_KEY, algorithms=["RS256"])
            request.user = data
        except Exception as e:
            return {"error": "Invalid token"}, 401
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.user["role"] != "admin":
            return {"error": "Forbidden"}, 403
        return f(*args, **kwargs)
    return decorated
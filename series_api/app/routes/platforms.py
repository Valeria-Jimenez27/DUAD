from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from app.routes import api_bp
from app.database import get_db
from app.models import Platform
from app.schemas import platform_to_dict


@api_bp.route("/platforms", methods=["POST"])
def create_platform():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    name = body.get("name", "").strip()
    if not name:
        return jsonify({"error": "'name' es requerido"}), 400

    try:
        with get_db() as db:
            platform = Platform(name=name)
            db.add(platform)
            db.flush()
            data = platform_to_dict(platform)
    except IntegrityError:
        return jsonify({"error": f"Ya existe una plataforma con el nombre '{name}'"}), 409
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify(data), 201

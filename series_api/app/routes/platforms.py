from flask import request, jsonify
from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError

from app.routes import api_bp
from app.database import get_db
from app.models import Platform, Series
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


@api_bp.route("/platforms/<string:platform_id>", methods=["PATCH"])
def update_platform(platform_id: str):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    name = body.get("name", "").strip()
    if not name:
        return jsonify({"error": "'name' es requerido"}), 400

    try:
        with get_db() as db:
            platform = db.get(Platform, platform_id)
            if platform is None:
                return jsonify({"error": f"Plataforma '{platform_id}' no encontrada"}), 404
            platform.name = name
            db.flush()
            data = platform_to_dict(platform)
    except IntegrityError:
        return jsonify({"error": f"Ya existe una plataforma con el nombre '{name}'"}), 409
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify(data)


@api_bp.route("/platforms/<string:platform_id>", methods=["DELETE"])
def delete_platform(platform_id: str):
    try:
        with get_db() as db:
            platform = db.get(Platform, platform_id)
            if platform is None:
                return jsonify({"error": f"Plataforma '{platform_id}' no encontrada"}), 404

            series_count = db.execute(
                select(func.count(Series.id)).where(Series.platform_id == platform_id)
            ).scalar_one()
            if series_count > 0:
                return jsonify({
                    "error": f"No se puede eliminar: {series_count} serie(s) usan esta plataforma"
                }), 409

            db.delete(platform)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return "", 204

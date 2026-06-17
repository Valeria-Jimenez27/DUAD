import re
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from app.routes import api_bp
from app.database import get_db
from app.models import Genre
from app.schemas import genre_to_dict


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


@api_bp.route("/genres", methods=["POST"])
def create_genre():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    name = body.get("name", "").strip()
    if not name:
        return jsonify({"error": "'name' es requerido"}), 400

    slug = body.get("slug", "").strip() or _slugify(name)

    try:
        with get_db() as db:
            genre = Genre(name=name, slug=slug)
            db.add(genre)
            db.flush()
            data = genre_to_dict(genre)
    except IntegrityError:
        return jsonify({"error": "Ya existe un género con ese nombre o slug"}), 409
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify(data), 201

import re
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError

from app.routes import api_bp
from app.database import get_db
from app.models import Genre
from app.schemas import genre_to_dict
from app.auth import require_auth


def _slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


@api_bp.route("/genres", methods=["POST"])
@require_auth
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


@api_bp.route("/genres/<string:genre_id>", methods=["PATCH"])
@require_auth
def update_genre(genre_id: str):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    try:
        with get_db() as db:
            genre = db.get(Genre, genre_id)
            if genre is None:
                return jsonify({"error": f"Género '{genre_id}' no encontrado"}), 404

            if "name" in body:
                name = body["name"].strip()
                if not name:
                    return jsonify({"error": "'name' no puede estar vacío"}), 400
                genre.name = name

            if "slug" in body:
                slug = body["slug"].strip() or _slugify(genre.name)
                genre.slug = slug
            elif "name" in body:
                genre.slug = _slugify(genre.name)

            db.flush()
            data = genre_to_dict(genre)
    except IntegrityError:
        return jsonify({"error": "Ya existe un género con ese nombre o slug"}), 409
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify(data)


@api_bp.route("/genres/<string:genre_id>", methods=["DELETE"])
@require_auth
def delete_genre(genre_id: str):
    try:
        with get_db() as db:
            genre = db.get(Genre, genre_id)
            if genre is None:
                return jsonify({"error": f"Género '{genre_id}' no encontrado"}), 404
            genre.series = []  # desvincula de todas las series antes de eliminar
            db.flush()
            db.delete(genre)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return "", 204

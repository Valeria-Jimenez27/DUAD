from flask import request, jsonify
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload, selectinload
from sqlalchemy.exc import IntegrityError

from app.routes import api_bp
from app.database import get_db
from app.models import Platform, Genre, Series, UserSeries, series_genres
from app.schemas import series_to_dict, tracking_to_dict
from app.auth import require_auth

VALID_STATUSES = {"completed", "watching", "dropped", "on_hold", "plan_to_watch"}


@api_bp.route("/series")
def get_series():
    try:
        page = max(1, int(request.args.get("page", 1)))
        per_page = min(100, max(1, int(request.args.get("per_page", 20))))
    except ValueError:
        return jsonify({"error": "page y per_page deben ser enteros"}), 400

    status = request.args.get("status")
    genre_slug = request.args.get("genre")
    platform_name = request.args.get("platform")

    conditions = []

    if status:
        conditions.append(
            Series.id.in_(select(UserSeries.series_id).where(UserSeries.status == status))
        )

    if genre_slug:
        conditions.append(
            Series.id.in_(
                select(series_genres.c.series_id)
                .join(Genre, Genre.id == series_genres.c.genre_id)
                .where(Genre.slug == genre_slug)
            )
        )

    if platform_name:
        conditions.append(
            Series.platform_id.in_(
                select(Platform.id).where(func.lower(Platform.name) == platform_name.lower())
            )
        )

    where_clause = and_(*conditions) if conditions else None

    try:
        with get_db() as db:
            count_stmt = select(func.count(Series.id))
            if where_clause is not None:
                count_stmt = count_stmt.where(where_clause)
            total = db.execute(count_stmt).scalar_one()

            stmt = (
                select(Series)
                .options(
                    joinedload(Series.platform),
                    selectinload(Series.genres),
                    joinedload(Series.user_series),
                )
                .order_by(Series.title)
                .offset((page - 1) * per_page)
                .limit(per_page)
            )
            if where_clause is not None:
                stmt = stmt.where(where_clause)

            series_list = db.execute(stmt).unique().scalars().all()
            # Serializar dentro de la sesión: db.commit() expira los objetos al salir
            data = [series_to_dict(s) for s in series_list]

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    pages = (total + per_page - 1) // per_page if total > 0 else 0

    return jsonify({
        "data": data,
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total": total,
            "pages": pages,
        },
    })


@api_bp.route("/series", methods=["POST"])
@require_auth
def create_series():
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    title = body.get("title", "").strip()
    if not title:
        return jsonify({"error": "'title' es requerido"}), 400

    year_start = body.get("year_start")
    if year_start is None:
        return jsonify({"error": "'year_start' es requerido"}), 400
    if not isinstance(year_start, int):
        return jsonify({"error": "'year_start' debe ser un entero"}), 400

    year_end = body.get("year_end")
    if year_end is not None and not isinstance(year_end, int):
        return jsonify({"error": "'year_end' debe ser un entero"}), 400

    total_seasons = body.get("total_seasons")
    if total_seasons is not None and not isinstance(total_seasons, int):
        return jsonify({"error": "'total_seasons' debe ser un entero"}), 400

    platform_id = body.get("platform_id")
    genre_ids = body.get("genre_ids", [])
    if not isinstance(genre_ids, list):
        return jsonify({"error": "'genre_ids' debe ser una lista"}), 400

    tracking_data = body.get("tracking")
    if tracking_data is not None:
        status = tracking_data.get("status", "").strip()
        if status not in VALID_STATUSES:
            return jsonify({
                "error": f"'status' inválido. Valores válidos: {', '.join(sorted(VALID_STATUSES))}"
            }), 400
        rating = tracking_data.get("rating")
        if rating is not None and (not isinstance(rating, int) or not (1 <= rating <= 5)):
            return jsonify({"error": "'rating' debe ser un entero entre 1 y 5"}), 400

    try:
        with get_db() as db:
            platform = None
            if platform_id:
                platform = db.get(Platform, platform_id)
                if platform is None:
                    return jsonify({"error": f"Plataforma con id '{platform_id}' no encontrada"}), 404

            genres = []
            for gid in genre_ids:
                genre = db.get(Genre, gid)
                if genre is None:
                    return jsonify({"error": f"Género con id '{gid}' no encontrado"}), 404
                genres.append(genre)

            series = Series(
                title=title,
                year_start=year_start,
                year_end=year_end,
                total_seasons=total_seasons,
                platform=platform,
                genres=genres,
            )
            db.add(series)
            db.flush()

            if tracking_data:
                db.add(UserSeries(
                    series_id=series.id,
                    status=tracking_data["status"],
                    seasons_watched=tracking_data.get("seasons_watched"),
                    episodes_watched=tracking_data.get("episodes_watched"),
                    rating=tracking_data.get("rating"),
                    review=tracking_data.get("review"),
                ))
                db.flush()

            data = series_to_dict(series)

    except IntegrityError:
        return jsonify({"error": "Ya existe una serie con ese título"}), 409
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify(data), 201


@api_bp.route("/series/<string:series_id>")
def get_series_by_id(series_id: str):
    stmt = (
        select(Series)
        .options(
            joinedload(Series.platform),
            selectinload(Series.genres),
            joinedload(Series.user_series),
        )
        .where(Series.id == series_id)
    )

    try:
        with get_db() as db:
            series = db.execute(stmt).unique().scalar_one_or_none()
            # Serializar dentro de la sesión por el mismo motivo que get_series()
            data = series_to_dict(series) if series is not None else None
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    if data is None:
        return jsonify({"error": f"Serie con id '{series_id}' no encontrada"}), 404

    return jsonify(data)


@api_bp.route("/series/<string:series_id>", methods=["PATCH"])
@require_auth
def update_series(series_id: str):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    year_end = body.get("year_end")
    if "year_end" in body and year_end is not None and not isinstance(year_end, int):
        return jsonify({"error": "'year_end' debe ser un entero"}), 400

    total_seasons = body.get("total_seasons")
    if "total_seasons" in body and total_seasons is not None and not isinstance(total_seasons, int):
        return jsonify({"error": "'total_seasons' debe ser un entero"}), 400

    genre_ids = body.get("genre_ids")
    if genre_ids is not None and not isinstance(genre_ids, list):
        return jsonify({"error": "'genre_ids' debe ser una lista"}), 400

    try:
        with get_db() as db:
            stmt = (
                select(Series)
                .options(joinedload(Series.platform), selectinload(Series.genres), joinedload(Series.user_series))
                .where(Series.id == series_id)
            )
            series = db.execute(stmt).unique().scalar_one_or_none()
            if series is None:
                return jsonify({"error": f"Serie '{series_id}' no encontrada"}), 404

            if "title" in body:
                title = body["title"].strip()
                if not title:
                    return jsonify({"error": "'title' no puede estar vacío"}), 400
                series.title = title

            if "year_start" in body:
                if not isinstance(body["year_start"], int):
                    return jsonify({"error": "'year_start' debe ser un entero"}), 400
                series.year_start = body["year_start"]

            if "year_end" in body:
                series.year_end = year_end

            if "total_seasons" in body:
                series.total_seasons = total_seasons

            if "platform_id" in body:
                pid = body["platform_id"]
                if pid is None:
                    series.platform = None
                    series.platform_id = None
                else:
                    platform = db.get(Platform, pid)
                    if platform is None:
                        return jsonify({"error": f"Plataforma '{pid}' no encontrada"}), 404
                    series.platform = platform

            if genre_ids is not None:
                genres = []
                for gid in genre_ids:
                    genre = db.get(Genre, gid)
                    if genre is None:
                        return jsonify({"error": f"Género '{gid}' no encontrado"}), 404
                    genres.append(genre)
                series.genres = genres

            db.flush()
            data = series_to_dict(series)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify(data)


@api_bp.route("/series/<string:series_id>/tracking", methods=["PATCH"])
@require_auth
def upsert_tracking(series_id: str):
    body = request.get_json(silent=True)
    if not body:
        return jsonify({"error": "Se esperaba un cuerpo JSON"}), 400

    if "status" in body:
        status = body["status"].strip() if body["status"] else ""
        if status not in VALID_STATUSES:
            return jsonify({
                "error": f"'status' inválido. Valores válidos: {', '.join(sorted(VALID_STATUSES))}"
            }), 400

    if "rating" in body and body["rating"] is not None:
        rating = body["rating"]
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return jsonify({"error": "'rating' debe ser un entero entre 1 y 5"}), 400

    try:
        with get_db() as db:
            series = db.get(Series, series_id)
            if series is None:
                return jsonify({"error": f"Serie '{series_id}' no encontrada"}), 404

            tracking = series.user_series
            if tracking is None:
                status = body.get("status", "").strip()
                if status not in VALID_STATUSES:
                    return jsonify({
                        "error": f"'status' es requerido para crear el tracking. Valores: {', '.join(sorted(VALID_STATUSES))}"
                    }), 400
                tracking = UserSeries(
                    series_id=series_id,
                    status=status,
                    seasons_watched=body.get("seasons_watched"),
                    episodes_watched=body.get("episodes_watched"),
                    rating=body.get("rating"),
                    review=body.get("review"),
                )
                db.add(tracking)
            else:
                if "status" in body:
                    tracking.status = body["status"].strip()
                if "seasons_watched" in body:
                    tracking.seasons_watched = body["seasons_watched"]
                if "episodes_watched" in body:
                    tracking.episodes_watched = body["episodes_watched"]
                if "rating" in body:
                    tracking.rating = body["rating"]
                if "review" in body:
                    tracking.review = body["review"]

            db.flush()
            data = tracking_to_dict(tracking)

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify(data)


@api_bp.route("/series/<string:series_id>", methods=["DELETE"])
@require_auth
def delete_series(series_id: str):
    try:
        with get_db() as db:
            series = db.get(Series, series_id)
            if series is None:
                return jsonify({"error": f"Serie '{series_id}' no encontrada"}), 404
            db.delete(series)  # cascade elimina el user_series asociado

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return "", 204


@api_bp.route("/stats")
def get_stats():
    try:
        with get_db() as db:
            total_series = db.execute(select(func.count(Series.id))).scalar_one()

            status_rows = db.execute(
                select(UserSeries.status, func.count(UserSeries.id))
                .group_by(UserSeries.status)
            ).all()
            status_dict = {row[0]: row[1] for row in status_rows}

            avg_rating = db.execute(
                select(func.avg(UserSeries.rating)).where(UserSeries.rating.is_not(None))
            ).scalar_one()

            top_genre_row = db.execute(
                select(Genre.name, func.count(series_genres.c.series_id).label("cnt"))
                .join(series_genres, Genre.id == series_genres.c.genre_id)
                .group_by(Genre.name)
                .order_by(func.count(series_genres.c.series_id).desc())
                .limit(1)
            ).first()

            top_platform_row = db.execute(
                select(Platform.name, func.count(Series.id).label("cnt"))
                .join(Series, Platform.id == Series.platform_id)
                .group_by(Platform.name)
                .order_by(func.count(Series.id).desc())
                .limit(1)
            ).first()

    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "detail": str(e)}), 500

    return jsonify({
        "total_series": total_series,
        "completed": status_dict.get("completed", 0),
        "watching": status_dict.get("watching", 0),
        "dropped": status_dict.get("dropped", 0),
        "on_hold": status_dict.get("on_hold", 0),
        "plan_to_watch": status_dict.get("plan_to_watch", 0),
        "average_rating": round(float(avg_rating), 1) if avg_rating is not None else None,
        "top_genre": top_genre_row[0] if top_genre_row else None,
        "top_platform": top_platform_row[0] if top_platform_row else None,
    })

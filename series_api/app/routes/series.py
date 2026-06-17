from flask import request, jsonify
from sqlalchemy import select, func, and_
from sqlalchemy.orm import joinedload, selectinload

from app.routes import api_bp
from app.database import get_db
from app.models import Platform, Genre, Series, UserSeries, series_genres
from app.schemas import series_to_dict


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

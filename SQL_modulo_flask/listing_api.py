from flask import Blueprint, request, jsonify
from base_de_datos import PgManager
listing_bp = Blueprint("listing_api", __name__)

def get_db():
    return PgManager("lyfter_car_rental", "postgres", "postgres", "localhost")


#para evitar ataques de inyeccion sql
ALLOWED_COLUMNS = {
    "users": [
        "id",
        "nombre",
        "email",
        "password",
        "username",
        "fecha_nacimiento",
        "estado"
    ],
    "cars": [
        "id",
        "marca",
        "modelo",
        "fecha_fabricacion",
        "estado"
    ],
    "rentals": [
        "id",
        "user_id",
        "car_id",
        "fecha_alquiler",
        "estado_alquiler"
    ]
}


def build_filter_query(table_name):
    base_query = f"SELECT * FROM {table_name}"
    filters = request.args
    if not filters:
        return base_query, []
    conditions = []
    values = []
    allowed_columns = ALLOWED_COLUMNS.get(table_name, [])
    for key, value in filters.items():
        if key not in allowed_columns:
            continue
        conditions.append(f"{key} = %s")
        values.append(value)
    if not conditions:
        return base_query, []
    where_clause = " AND ".join(conditions)
    final_query = f"{base_query} WHERE {where_clause}"
    return final_query, values


def list_data(table_name):
    db = None
    try:
        db = get_db()
        query, values = build_filter_query(table_name)
        result = db.execute(query, values, fetch=True)
        return jsonify(result), 200
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
    finally:
        if db:
            db.close()


@listing_bp.route("/users", methods=["GET"])
def list_users():
    return list_data("users")


@listing_bp.route("/cars", methods=["GET"])
def list_cars():
    return list_data("cars")


@listing_bp.route("/rentals", methods=["GET"])
def list_rentals():
    return list_data("rentals")

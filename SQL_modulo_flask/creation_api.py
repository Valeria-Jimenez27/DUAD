from flask import Blueprint, request, jsonify
from base_de_datos import PgManager

creation_bp = Blueprint("creation_api", __name__)

def get_db():
    return PgManager("lyfter_car_rental", "postgres", "postgres", "localhost")

# Crear usuario
@creation_bp.route("/users", methods=["POST"])
def create_user():
    data = request.json
    db = get_db()
    if not db.connection:
        return jsonify({"error": "Database connection failed"}), 500
    query = """
        INSERT INTO users (nombre, email, username, password, fecha_nacimiento, estado)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    try:
        db.execute(query, (
            data["nombre"],
            data["email"],
            data["username"],
            data["password"],
            data["fecha_nacimiento"],
            data["estado"]
        ))
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        db.close()

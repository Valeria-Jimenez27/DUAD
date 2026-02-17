from flask import Blueprint, request, jsonify
from base_de_datos import PgManager


db = PgManager(
    db_name="lyfter_car_rental",
    user="postgres",
    password="postgres",
    host="localhost"
)
users_bp = Blueprint("users", __name__)

#Repositorio de usuarios
class UserRepository:
    @staticmethod
    def create(user_data):
        query = """
            INSERT INTO lyfter_car_rental.users(nombre, email, username, password, fecha_nacimiento, estado)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        params = (
            user_data["full_name"],
            user_data["email"],
            user_data["username"],
            user_data["password"],
            user_data["fecha_nacimiento"],
            user_data["estado"]
        )
        result = db.execute(query, params, fetch=True)
        return result[0]["id"] if result else None

    @staticmethod
    def update_estado(user_id, status):
        query = """
            UPDATE lyfter_car_rental.users
            SET estado = %s
            WHERE id = %s;
        """
        db.execute(query, (status, user_id))


    @staticmethod
    def check_moroso(user_id):
        query = """
            UPDATE lyfter_car_rental.users
            SET is_moroso = TRUE
            WHERE id = %s;
        """
        db.execute(query, (user_id,))


    @staticmethod
    def get_all(filters):
        query = "SELECT * FROM lyfter_car_rental.users WHERE 1=1"
        values = []
        allowed_filters = [
            "id", "nombre", "email",
            "username", "estado", "es_moroso"
        ]
        for key, value in filters.items():
            if key in allowed_filters:
                query += f" AND {key} = %s"
                values.append(value)
        return db.execute(query, values, fetch=True)
    

#Endpoints de usuarios
@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        required_fields = [
            "nombre",
            "email",
            "username",
            "password",
            "fecha_nacimiento",
            "estado"
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        user_id = UserRepository.create(data)
        if not user_id:
            return jsonify({"error": "User could not be created"}), 400
        return jsonify({
            "message": f"User {user_id} created successfully",
        }), 201
    except Exception as e:
        return jsonify({
            "error": "Error creating user",
            "details": str(e)
        }), 500

@users_bp.route("/<int:user_id>/estado", methods=["PATCH"])
def change_estado(user_id):
    try:
        data = request.get_json()
        if "estado" not in data:
            return jsonify({"error": "estado is required"}), 400
        UserRepository.update_estado(user_id, data["estado"])
        return jsonify({"message": "Estado actualizado exitosamente"}), 200
    except Exception as e:
        return jsonify({
            "error": "Error updating estado",
            "details": str(e)
        }), 500

@users_bp.route("/<int:user_id>/moroso", methods=["PATCH"])
def flag_moroso(user_id):
    try:
        UserRepository.check_moroso(user_id)
        return jsonify({
            "message": "User flagged as moroso"
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Error flagging user",
            "details": str(e)
        }), 500

@users_bp.route("/", methods=["GET"])
def list_users():
    try:
        filters=request.args
        users = UserRepository.get_all(filters)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({
            "error": "Error listing users",
            "details": str(e)
        }), 500



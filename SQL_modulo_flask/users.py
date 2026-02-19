from flask import Blueprint, request, jsonify
from base_de_datos import db

users_bp = Blueprint("users", __name__)

class UserRepository:
    @staticmethod
    def create(data):
        query = """
            INSERT INTO lyfter_car_rental.users
            (name, email, username, password, birth_date, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        params = (
            data["name"],
            data["email"],
            data["username"],
            data["password"],
            data["birth_date"],
            data["status"]
        )
        result = db.execute(query, params, fetch=True)
        return result[0]["id"]


    @staticmethod
    def update(user_id, fields):
        query = "UPDATE lyfter_car_rental.users SET "
        values = []
        for key, value in fields.items():
            query += f"{key} = %s, "
            values.append(value)
        query = query.rstrip(", ")
        query += " WHERE id = %s;"
        values.append(user_id)
        db.execute(query, values)

    @staticmethod
    def get_by_id(user_id):
        result = db.execute(
            "SELECT id FROM lyfter_car_rental.users WHERE id = %s;",
            (user_id,),
            fetch=True
        )
        return bool(result)

    @staticmethod
    def get_all(filters):
        query = "SELECT * FROM lyfter_car_rental.users WHERE 1=1"
        values = []
        allowed = ["id", "name", "email", "username", "birth_date", "status"]
        for key, value in filters.items():
            if key in allowed:
                query += f" AND {key} = %s"
                values.append(value)
        return db.execute(query, values, fetch=True)


#Endpoints de users
@users_bp.route("/", methods=["POST"])
def create_user():
    try:
        data = request.get_json()
        required = ["name", "email", "username", "password", "birth_date", "status"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        user_id = UserRepository.create(data)
        return jsonify({
            "message": "User created successfully",
            "user_id": user_id
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_bp.route("/<int:user_id>", methods=["PATCH"])
def update_user(user_id):
    try:
        data = request.get_json()
        if not UserRepository.get_by_id(user_id):
            return jsonify({"error": "User not found"}), 404
        UserRepository.update(user_id, data)
        return jsonify({"message": "User updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@users_bp.route("/", methods=["GET"])
def list_users():
    try:
        filters = request.args.to_dict()
        users = UserRepository.get_all(filters)
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

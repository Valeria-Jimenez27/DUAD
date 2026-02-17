from flask import Blueprint, request, jsonify
from base_de_datos import PgManager
from datetime import datetime


db = PgManager(
    db_name="lyfter_car_rental",
    user="postgres",
    password="postgres",
    host="localhost"
)

rentals_bp = Blueprint("rentals", __name__)

#Repositorio de rentals
class RentalRepository:
    @staticmethod
    def create_rental(rental_data):
        query = """
            INSERT INTO lyfter_car_rental.rentals (user_id, car_id, estado_alquiler)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        params = (
            rental_data["user_id"],
            rental_data["car_id"],
            rental_data["estado_alquiler"]
        )
        result = db.execute(query, params, fetch=True)
        return result[0]["id"] if result else None


    @staticmethod
    def update_estado_alquiler(rental_id, estado_alquiler):
        query = """
            UPDATE lyfter_car_rental.rentals
            SET estado_alquiler = %s
            WHERE id = %s;
        """
        db.execute(query, (estado_alquiler, rental_id))


    @staticmethod
    def complete_rental(rental_id):
        query = """
            UPDATE lyfter_car_rental.rentals
            SET estado = 'completado'
            WHERE id = %s;
        """
        db.execute(query, (rental_id,))


    @staticmethod
    def get_all(filters):
        query = "SELECT * FROM lyfter_car_rental.rentals WHERE 1=1"
        values = []
        allowed_filters = [
            "id", "user_id", "car_id",
            "fecha_alquiler", "estado_alquiler"
        ]
        for key, value in filters.items():
            if key in allowed_filters:
                query += f" AND {key} = %s"
                values.append(value)
        return db.execute(query, values, fetch=True)


#ENDPOINTS DE RENTALS
@rentals_bp.route("/", methods=["POST"])
def create_rental():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        required_fields = ["user_id", "car_id", "estado_alquiler"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"{field} is required"}), 400
        rental_id = RentalRepository.create_rental(data)
        return jsonify({
            "message": f"Rental created successfully with ID: {rental_id}"
        }), 201
    except Exception as e:
        return jsonify({
            "error": "Error creating rental",
            "details": str(e)
        }), 500

@rentals_bp.route("/<int:rental_id>/estado_alquiler", methods=["PATCH"])
def update_rental_estado_alquiler(rental_id):
    try:
        data = request.get_json()
        if not data or "estado_alquiler" not in data:
            return jsonify({"error": "estado_alquiler is required"}), 400
        RentalRepository.update_estado_alquiler(rental_id, data["estado_alquiler"])
        return jsonify({
            "message": "Estado_alquiler updated successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Error updating rental estado_alquiler",
            "details": str(e)
        }), 500

@rentals_bp.route("/<int:rental_id>/complete", methods=["PATCH"])
def complete_rental(rental_id):
    try:
        RentalRepository.complete_rental(rental_id)
        return jsonify({
            "message": "Rental completed successfully"
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Error completing rental",
            "details": str(e)
        }), 500

@rentals_bp.route("/", methods=["GET"])
def list_rentals():
    try:
        filters = request.args.to_dict()
        rentals = RentalRepository.get_all(filters)
        return jsonify(rentals), 200
    except Exception as e:
        return jsonify({
            "error": "Error listing rentals",
            "details": str(e)
        }), 500

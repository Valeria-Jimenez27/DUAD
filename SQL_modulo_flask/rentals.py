from flask import Blueprint, request, jsonify
from base_de_datos import db
from cars import CarRepository
from users import UserRepository

rentals_bp = Blueprint("rentals", __name__)


class RentalRepository:
    @staticmethod
    def create(data):
        query = """
            INSERT INTO lyfter_car_rental.rentals
            (user_id, car_id, rental_status)
            VALUES (%s, %s, %s)
            RETURNING id;
        """
        params = (
            data["user_id"],
            data["car_id"],
            data["rental_status"]
        )
        result = db.execute(query, params, fetch=True)
        return result[0]["id"]

    @staticmethod
    def update(rental_id, fields):
        query = "UPDATE lyfter_car_rental.rentals SET "
        values = []
        for key, value in fields.items():
            query += f"{key} = %s, "
            values.append(value)
        query = query.rstrip(", ")
        query += " WHERE id = %s;"
        values.append(rental_id)
        db.execute(query, values)

    @staticmethod
    def get_by_id(rental_id):
        result = db.execute(
            "SELECT * FROM lyfter_car_rental.rentals WHERE id = %s;",
            (rental_id,),
            fetch=True
        )
        return result[0] if result else None

    @staticmethod
    def get_all(filters):
        query = "SELECT * FROM lyfter_car_rental.rentals WHERE 1=1"
        values = []
        allowed = ["id", "user_id", "car_id", "rental_status"]
        for key, value in filters.items():
            if key in allowed:
                query += f" AND {key} = %s"
                values.append(value)
        return db.execute(query, values, fetch=True)


# Endpoints de rentals
@rentals_bp.route("/", methods=["POST"])
def create_rental():
    try:
        data = request.get_json()
        required = ["user_id", "car_id"]
        for field in required:
            if field not in data:
                return jsonify({"error": f"{field} is required"}), 400
        if not UserRepository.get_by_id(data["user_id"]):
            return jsonify({"error": "User not found"}), 404
        car = CarRepository.get_by_id(data["car_id"])
        if not car:
            return jsonify({"error": "Car not found"}), 404
        if car["car_status"].strip().lower() != "available":
            return jsonify({"error": "Car not available"}), 400
        
        rental_data = {
            "user_id": data["user_id"],
            "car_id": data["car_id"],
            "rental_status": "active"
        }
        rental_id = RentalRepository.create(rental_data)
        CarRepository.update(data["car_id"], {"car_status": "rented"})
        return jsonify({
            "message": f"Rental created successfully with ID: {rental_id}"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@rentals_bp.route("/<int:rental_id>", methods=["PATCH"])
def update_rental(rental_id):
    try:
        rental = RentalRepository.get_by_id(rental_id)

        if not rental:
            return jsonify({"error": "Rental not found"}), 404

        data = request.get_json()
#Aca comprueblo si se completo el alquiler para cambiar el estado del auto a disponible
        if "rental_status" in data and data["rental_status"] == "completed":
            CarRepository.update(rental["car_id"], {"car_status": "available"})
        RentalRepository.update(rental_id, data)
        return jsonify({"message": "Rental updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@rentals_bp.route("/", methods=["GET"])
def list_rentals():
    try:
        filters = request.args.to_dict()
        rentals = RentalRepository.get_all(filters)
        return jsonify(rentals), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
